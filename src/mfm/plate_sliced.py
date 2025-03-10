import zipfile, re, typing, queue, io, enum, os

from .configuration import *
from .map_post_process import *
from .line_ending import *

# AMS remapping in Print dialog requires
# N settings for N colors in Metadata/project_settings.config
# N <filament> for N colors in Metadata/slice_info.config

class FileExtensions(enum.Enum):
    UNKNOWN = "unknown"
    GCODE = ".gcode"
    THREEMF = ".3mf"

PLATE_N = 'plate_\d+.gcode$'

def zipFilePointerForZip(zipPath: str, write: bool):
  return zipfile.ZipFile(zipPath, 'w' if write else 'r')

# Adapted from https://medium.com/dev-bits/ultimate-guide-for-working-with-i-o-streams-and-zip-archives-in-python-3-6f3cf96dca50
def processAllPlateGcodeForZipFile(inputZip: zipfile.ZipFile, out: typing.TextIO, configuration: MFMConfiguration, statusQueue: queue.Queue):
  startTime = time.monotonic()
  new_zip = io.BytesIO()

  with zipfile.ZipFile(new_zip, 'w') as new_archive:
    platesProcessed = 0
    for item in inputZip.filelist:
      # If you spot an existing file, create a new object
      if re.match(PLATE_N, os.path.basename(item.filename)):
        if statusQueue:
          sqItem = StatusQueueItem()
          sqItem.statusLeft = f"{os.path.basename(item.filename)}"
          sqItem.statusRight = f"Starting"
          sqItem.progress = 0
          statusQueue.put(item=sqItem)
        
        zi = zipfile.ZipInfo(item.filename)
        
        tmpGcodeFilename = os.path.basename(item.filename)
        tmpGcodeFile = open(tmpGcodeFilename, mode='w')
        
        # Detect line ending of Gcode file
        if configuration[CONFIG_LINE_ENDING] == LineEnding.AUTODETECT.value:
          lineEndingFlavor = LineEnding.AUTODETECT
          with io.BytesIO(initial_bytes=inputZip.read(item.filename)) as gcodeBytes:
            lineEndingFlavor = determineLineEndingTypeInFile(fb=gcodeBytes)
            print(f"Detected {repr(lineEndingFlavor)} line ending in input file {zi.filename}.")
          if lineEndingFlavor == LineEnding.UNKNOWN:
            lineEndingFlavor = LineEnding.UNIX
            print(f"Defaulting to {LINE_ENDING_UNIX_TITLE}")
          configuration[CONFIG_LINE_ENDING] = lineEndingFlavor.value

        with io.TextIOWrapper(io.BytesIO(initial_bytes=inputZip.read(item.filename))) as gcodeText:
          process(configuration=configuration, inputFP=gcodeText, outputFP=tmpGcodeFile, statusQueue=statusQueue)
        
        # Zipfile implementation of seek is too slow because it restarts from start of file each time
        # https://stackoverflow.com/questions/51801213/complexity-of-f-seek-in-python/51801243
        #process(configuration=configuration, inputFP=io.TextIOWrapper(inputZip.open(zi.filename, mode='r')), outputFP=tmpGcodeFile, statusQueue=statusQueue)
        
        if statusQueue:
          sqItem = StatusQueueItem()
          sqItem.statusLeft = f"{os.path.basename(item.filename)}"
          sqItem.statusRight = f"Compressing"
          sqItem.progress = 50
          statusQueue.put(item=sqItem)
        
        new_archive.write(tmpGcodeFilename, arcname=item.filename, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        platesProcessed += 1
      else:
        if statusQueue:
          sqItem = StatusQueueItem()
          sqItem.statusLeft = f"{os.path.basename(item.filename)}"
          sqItem.statusRight = f"Compressing"
          sqItem.progress = 50
          statusQueue.put(item=sqItem)
        
        # Copy other contents as it is
        # Bambu Studio only supports DEFLATE compression
        new_archive.writestr(item, inputZip.read(item.filename), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

  if statusQueue:
    sqItem = StatusQueueItem()
    sqItem.statusLeft = f"{os.path.basename(configuration[CONFIG_INPUT_FILE])}"
    sqItem.statusRight = f"Saving"
    sqItem.progress = 75
    statusQueue.put(item=sqItem)

  out.write(new_zip.getbuffer())
  
  if statusQueue:
    sqItem = StatusQueueItem()
    sqItem.statusRight = f"Completed all {platesProcessed} plate sliced G-code{'s' if platesProcessed > 0 else ''} in {str(datetime.timedelta(seconds=time.monotonic()-startTime))}s" if platesProcessed > 0 else "Did not find any plate sliced G-code to process."
    sqItem.progress = 100
    statusQueue.put(item=sqItem)

def allPlateGcodeFilePointersForZipFile(z: zipfile.ZipFile) -> list[typing.TextIO]:
  plateGcodeFilePointers = []
  
  for zi in z.infolist():
    if re.match(PLATE_N, zi.filename):
      plateGcodeFilePointers.append(io.TextIOWrapper(z.open(zi)))
