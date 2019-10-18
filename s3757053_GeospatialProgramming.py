#Analysis of demographics of Indians in Melbourne and Accessibility to religious Institutions
#s3757053_Shalika_Dharmasthala
#Geospatial_Programming

#Import processing.qgis and math Classes
from qgis.core import *
from qgis.PyQt.QtCore import QVariant
import processing 

# Define path for input layers
input_filepath = "H:/Sem 2/Sem2_ GIS Programming/Major Project/Data/"
# Define input layer names
localitymap_filename = "VIC_LOCALITY_POLYGON_shp.shp" # Define locality layer name
urbanExtent_filename = "UrbanExtent2015_region.shp" # Define urban extent layer name
church_filename = "church.shp" # Define church layer name
temple_filename = "Temple.shp" # Define Temple layer name
Mosque_filename = "Mosque.shp" # Define Mosque layer name
Density_filename = "Indian_Density.shp"# Define population layer name
road_filename = "Road.shp"# Define road layer name


# Define path for input layers
output_filepath = "H:/Sem 2/Sem2_ GIS Programming/Major Project/outputs/"
# Define output layer names
fixed_locality= "fixed_locality.shp" #File to save fixed geomfile
fixed_Urbanextent= "fixed_Urbanextent.shp" #File to save fixed geomfile
extract_output = "intersection.shp" #File to save intersected file
road_output = "road_Intersect.shp" #File to save intersected file
church_bufferout = "church_buffer.shp"
merge_output = "FOI_layer.shp" # File to save merged feature of interest layer
buffer_output = "buffer.shp" # File to save buffer output
clip_output = "network.shp" # File to save clipped area
final_network = "road_distance.shp" # File to save intersected road

# Define variables
church = input_filepath +church_filename
temple = input_filepath +temple_filename
mosque = input_filepath +Mosque_filename



#Create dictionaries to define parameters
Locality_dict = {'INPUT':input_filepath + localitymap_filename,  'OUTPUT':output_filepath + fixed_locality}
urbanextent_dict = {'INPUT': input_filepath + urbanExtent_filename ,  'OUTPUT':output_filepath + fixed_Urbanextent}
extract_dict = {'INPUT': output_filepath + fixed_locality,'PREDICATE': 0,'INTERSECT':output_filepath + fixed_Urbanextent,'OUTPUT':output_filepath + extract_output }
extractroad_dict = {'INPUT': input_filepath + road_filename,'PREDICATE': 0,'INTERSECT':output_filepath + extract_output,'OUTPUT':output_filepath + road_output }
merge_dict = {'LAYERS': [church,temple,mosque] ,'OUTPUT':output_filepath + merge_output }
buffer_dict = {'SHAPES': output_filepath + merge_output,'DIST_FIELD_DEFAULT': 5000,'NZONES': 5,'BUFFER' :output_filepath + buffer_output }
network_dict =  {'INPUT':output_filepath + road_output,  'OVERLAY':output_filepath + buffer_output,'OUTPUT':output_filepath + clip_output }
final_network_dict = {'INPUT': output_filepath + clip_output,'JOIN': output_filepath + buffer_output,'PREDICATE':0,'METHOD':0, 'OUTPUT':output_filepath + final_network  }

# Add layers to view
#locality_layer= iface.addVectorLayer(input_filepath + localitymap_filename , localitymap_filename[:-4], 'ogr')
#urbanextent_layer= iface.addVectorLayer(input_filepath + urbanExtent_filename , urbanExtent_filename[:-4], 'ogr')
church_layer= iface.addVectorLayer(input_filepath + church_filename , church_filename[:-4], 'ogr')
temple_layer= iface.addVectorLayer(input_filepath + temple_filename , temple_filename[:-4], 'ogr')
mosque_layer= iface.addVectorLayer(input_filepath + Mosque_filename , Mosque_filename[:-4], 'ogr')
population_layer= iface.addVectorLayer(input_filepath + Density_filename , Density_filename[:-4], 'ogr')




#Fix Geometries
Locality_Geom = processing.run('native:fixgeometries', Locality_dict)
#iface.addVectorLayer(fixed_locality,'','ogr')

#Fix Geometries
Urbanextent_Geom= processing.run('native:fixgeometries',urbanextent_dict)
#iface.addVectorLayer(fixed_Urbanextent,'','ogr')

#Use extract by localities which are intersect with the urban growth boundary
extract_locality = processing.run('native:extractbylocation',extract_dict)

lyr=iface.addVectorLayer(output_filepath + extract_output,'','ogr')
lyr.setOpacity(0.3)# Layer opacity

#switch on labelling and set label appearence
layer_settings  = QgsPalLayerSettings()
text_format = QgsTextFormat()

text_format.setFont(QFont("Arial", 8)) # Set font and font size
text_format.setSize(8)


layer_settings.setFormat(text_format)

layer_settings.fieldName = "VIC_LOCA_2" #Set field for labelling
layer_settings.placement = 2

layer_settings.enabled = True

layer_settings = QgsVectorLayerSimpleLabeling(layer_settings)
lyr.setLabelsEnabled(True)#Enable labelling
lyr.setLabeling(layer_settings)#set labelling
lyr.triggerRepaint()
print("labelling enabled")


# extract roads which are within locality boundary
extract_road = processing.run('native:extractbylocation',extractroad_dict)
iface.addVectorLayer(output_filepath + road_output,'','ogr')
#del Intersect #Delete file in temp

# Merge Relious institutions layer
merge_layers = processing.run("native:mergevectorlayers",merge_dict)
#iface.addVectorLayer(output_filepath + merge_output,'','ogr')

#Create multiple buffers with define distances
multi_buffer = processing.run("saga:fixeddistancebuffer",buffer_dict)
#buffer_layer= iface.addVectorLayer(output_filepath + buffer_output,'','ogr')
print("Buffer created")

#Clip road to buffer layer
clip = processing.run("native:clip",network_dict)
#iface.addVectorLayer(output_filepath + clip_output,'','ogr')

#Join road and buffer layer
join = processing.run("qgis:joinattributesbylocation",final_network_dict)
network_layer = iface.addVectorLayer(output_filepath + final_network,'','ogr')
lyr.setOpacity(0.2)
print("network layer created")

target_field = "suburb_I_1"

#Change symbology of the intersected layer with locality and urban extent boundaries to show difference in population
def apply_graduated_symbology():
    """Creates Symbology for each value in range of values. 
        Values are # of Indians per locality."""
        
    myRangeList = []

    symbol = QgsSymbol.defaultSymbol(population_layer.geometryType())     
    symbol.setColor(QColor("#ffffcc"))   # Define colour to be applied                            
    myRange = QgsRendererRange(0, 660, symbol, '0 - 660')  # Define range                 
    myRangeList.append(myRange) # Append list                                    

    symbol = QgsSymbol.defaultSymbol(population_layer.geometryType())
    symbol.setColor(QColor("#a1dab4")) # Define colour to be applied 
    myRange = QgsRendererRange(661, 1600, symbol, '661 - 1600')# Define range
    myRangeList.append(myRange)# Append list
    
    symbol = QgsSymbol.defaultSymbol(population_layer.geometryType())
    symbol.setColor(QColor("#41b6c4")) # Define colour to be applied 
    myRange = QgsRendererRange(1601, 3300, symbol, '1601 - 3300')# Define range
    myRangeList.append(myRange)# Append list
    
    symbol = QgsSymbol.defaultSymbol(population_layer.geometryType())
    symbol.setColor(QColor("#2c7fb8")) # Define colour to be applied 
    myRange = QgsRendererRange(3301, 6700, symbol, '3301 - 6700')# Define range
    myRangeList.append(myRange)# Append list
    
    symbol = QgsSymbol.defaultSymbol(population_layer.geometryType())
    symbol.setColor(QColor("#253494")) # Define colour to be applied 
    myRange = QgsRendererRange(6701, 13800, symbol, '6701 - 13800')# Define range
    myRangeList.append(myRange)# Append list

    myRenderer = QgsGraduatedSymbolRenderer(target_field, myRangeList)  
    myRenderer.setMode(QgsGraduatedSymbolRenderer.Custom)               

    population_layer.setRenderer(myRenderer)                                  
    
    print(f"Graduated color scheme applied")

apply_graduated_symbology()# Apply symbology to layer

target_field_buffer = "ID"
def apply_buffer_symbology():
    """Creates Symbology for each value in range of values. 
        Values are buffer distances."""
        
    myRangeList = []

    symbol = QgsSymbol.defaultSymbol(network_layer.geometryType())     
    symbol.setColor(QColor("#fef0d9"))   # Define colour to be applied                             
    myRange = QgsRendererRange(1, 2, symbol, '0 - 1000')  # Define range                 
    myRangeList.append(myRange)# Append list                                     

    symbol = QgsSymbol.defaultSymbol(network_layer.geometryType())
    symbol.setColor(QColor("#fdcc8a")) # Define colour to be applied 
    myRange = QgsRendererRange(2.1, 3, symbol, '1001 - 2000')# Define range
    myRangeList.append(myRange)# Append list
    
    symbol = QgsSymbol.defaultSymbol(network_layer.geometryType())
    symbol.setColor(QColor("#fc8d59")) # Define colour to be applied 
    myRange = QgsRendererRange(3.1, 4, symbol, '2001 - 3000')# Define range
    myRangeList.append(myRange)# Append list
    
    symbol = QgsSymbol.defaultSymbol(network_layer.geometryType())
    symbol.setColor(QColor("#e34a33")) # Define colour to be applied 
    myRange = QgsRendererRange(4.1, 5, symbol, '3001 - 4000')# Define range
    myRangeList.append(myRange)# Append list
    
    symbol = QgsSymbol.defaultSymbol(network_layer.geometryType())
    symbol.setColor(QColor("#b30000")) # Define colour to be applied 
    myRange = QgsRendererRange(5.1, 6, symbol, '4001 - 5000')# Define range
    myRangeList.append(myRange)# Append list

    myRenderer = QgsGraduatedSymbolRenderer(target_field_buffer, myRangeList)  
    myRenderer.setMode(QgsGraduatedSymbolRenderer.Custom)               

    network_layer.setRenderer(myRenderer)                                  
    
    print(f"Graduated color scheme applied")

apply_buffer_symbology()# Apply symbology to layer


