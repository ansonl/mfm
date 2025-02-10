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

# https://medium.com/dev-bits/ultimate-guide-for-working-with-i-o-streams-and-zip-archives-in-python-3-6f3cf96dca50
def processAllPlateGcodeForZipFile(inputZip: zipfile.ZipFile, out: typing.TextIO, configuration: MFMConfiguration, statusQueue: queue.Queue):
  new_zip = io.BytesIO()

  with zipfile.ZipFile(new_zip, 'w') as new_archive:
    for item in inputZip.filelist:
      # If you spot an existing file, create a new object
      if re.match(PLATE_N, os.path.basename(item.filename)):
        if statusQueue:
          item = StatusQueueItem()
          item.statusLeft = f"{os.path.basename(item.filename)}"
          item.statusRight = f"Starting"
          item.progress = 0
          statusQueue.put(item=item)
        
        zi = zipfile.ZipInfo(item.filename)
        
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
        
        tmpGcodeFilename = os.path.basename(item.filename)
        tmpGcodeFile = open(tmpGcodeFilename, mode='w')
        
        process(configuration=configuration, inputFP=io.TextIOWrapper(inputZip.open(zi.filename, mode='r')), outputFP=tmpGcodeFile, statusQueue=statusQueue)
        
        new_archive.write(tmpGcodeFilename, arcname=item.filename)
      else:
        # Copy other contents as it is
        new_archive.writestr(item, inputZip.read(item.filename))

  out.write(new_zip.getbuffer())

def allPlateGcodeFilePointersForZipFile(z: zipfile.ZipFile) -> list[typing.TextIO]:
  plateGcodeFilePointers = []
  
  for zi in z.infolist():
    if re.match(PLATE_N, zi.filename):
      plateGcodeFilePointers.append(io.TextIOWrapper(z.open(zi)))
