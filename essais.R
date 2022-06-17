
library(reticulate)
#library(tiff)
# library(imager)
library(raster)
## Loading required package: sp
#virtualenv_create("r-reticulate")
virtualenv_install("r-reticulate", "opencv-python")
virtualenv_install("r-reticulate", "tifffile")
virtualenv_install("r-reticulate", "scikit-image")
virtualenv_install("r-reticulate", "matplotlib")
#virtualenv_list() 
#py_discover_config()

# reticulate::import_from_path("cv2", path = "C:/Users/tprimet/AppData/Local/r-miniconda/envs/r-reticulate/Lib/site-packages/cv2", delay_load = FALSE)
reticulate::import_from_path("cv2", path = "C:/Users/tprimet/Documents/.virtualenvs/r-reticulate/Lib/site-packages/cv2", delay_load = FALSE)
reticulate::import_from_path("tifffile", path = "C:/Users/tprimet/Documents/.virtualenvs/r-reticulate/Lib/site-packages/tifffile", delay_load = FALSE)
reticulate::import_from_path("matplotlib" , path = "C:/Users/tprimet/AppData/Local/r-miniconda/envs/r-reticulate/Lib/site-packages/matplotlib",  delay_load = FALSE)
reticulate::import_from_path("skimage" , path = "C:/Users/tprimet/AppData/Local/r-miniconda/envs/r-reticulate/Lib/site-packages/skimage",  delay_load = FALSE)
#use_virtualenv
cv = import("cv2")
tif = import("tifffile")
skimage = import("skimage")
py_install(packages = "matplotlib")
py_install(packages = "scikit-image")
flat = import("flatten")
shift = import('cross_correlation_shift')
# source_python('compileScript.py')
# liste_dossier = compile_script()
# liste_dossier
arrange_channels <- function(x) {
  ms1 <- sort(x[grep("MS1_", x)])
  ms2 <- sort(x[grep("MS2_", x)])
  c(ms1, ms2)
}
as_raster <- function(x, xmx = 426, ymx = 339) {
  if(is.matrix(x)) {
    r <- raster::raster(x, xmn=0, xmx=xmx, ymn=0, ymx=ymx)
  } else {
    r <- raster::stack(apply(x, 3, raster::raster, xmn=0, xmx=xmx, ymn=0, ymx=ymx))
  }
  r
}
#MS2
base_path = "C:/Users/tprimet/Documents/REPRISE/MS/MS2_unziped/20220519_134340"
all_files <- list.files(base_path, pattern = "img", full.names = TRUE)
cubestack <- stack((arrange_channels(all_files)))
plotRGB(cubestack, scale = 255, stretch = "lin")
tmp <- tempdir()
# band_files <- list.files(tmp, pattern = tools::file_path_sans_ext(basename(base_path)), full.names = TRUE)
xml_PathName = "C:/Users/tprimet/Documents/REPRISE/XML/MatriceMS1.xml"
flattened1 <- lapply(all_files, function(x) flat$flatten(x, xml_PathName))
cubestackFlat <- raster::stack(lapply(flattened1, as_raster))
plotRGB(cubestackFlat, scale = 255, stretch = "lin")


#MS1
base_path = "C:/Users/tprimet/Documents/REPRISE/MS/MS1_unziped/20220519_134340"
all_files <- list.files(base_path, pattern = "img", full.names = TRUE)
cubestack <- stack((arrange_channels(all_files)))
plotRGB(cubestack, scale = 255, stretch = "lin")


# band_files <- list.files(tmp, pattern = tools::file_path_sans_ext(basename(base_path)), full.names = TRUE)
xml_PathName = "C:/Users/tprimet/Documents/REPRISE/XML/MatriceMS1.xml"
flattened2 <- lapply(all_files, function(x) flat$flatten(x, xml_PathName))
cubestackFlat <- raster::stack(lapply(flattened2, as_raster))

plotRGB(cubestackFlat, scale = 255, stretch = "lin")
#shift$cross_correlation_shift(flattened1[1],flattened2[1] )
shiffted = lapply(flattened2, function(x) shift$cross_correlation_shift(flattened1[9], x))
#shiffted = lapply(shift$cross_correlation_shift,flattened1,flattened2 )
cubestackshift <- raster::stack(lapply(shift, as_raster))
