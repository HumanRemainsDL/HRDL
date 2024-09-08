#import packages
from pdf2image import convert_from_path 
from tesserocr import PyTessBaseAPI

#Path of the directory where the files to be OCRed are located.
input_dir_l='/...'

#Path of the directory where you want the sequenced pdf files to be stored.
output_dir_l='/...'

#Path of the directory where you want the output text files to be stored.
output_dir_l_ocr='/...'

def batch_pdf_text_regions(input_dir_l, output_dir_l):
    #If the output directory does not already exist, create it
    if not os.path.exists(output_dir_l):
        os.mkdir(output_dir_l)
    
    #Iterate through filenames in local directory
    for filename in os.listdir(input_dir_l):
        if filename.endswith('.pdf'):
            print(filename)
            #Create a list of PIL image files where each page of the file is one element of the list
            pages = convert_from_path(os.path.join(input_dir_l, filename))
            
            #Instantiate an empty list of images
            lim=[]
            #Create a path where to store the output file
            new_filepath=os.path.join(output_dir_l, filename)

            #For each page, a list called 'regions' is created. Each element of the list is a tuple containing the image of one of the regions and a dictionary containing the 4 coordinates of the region (the 'x' and 'y' coordinates of the top-left corner as well as the height and the width).
            #For region of each page, a new image is created by cropping the page according to the fours coordinates of the regions. Each image is saved onto the list initiated above.
            for p in pages:
                with PyTessBaseAPI() as api:
                    api.SetImage(p)
                    regions = api.GetRegions()
                    for (im, box) in regions:
                        lim.append(p.crop((box['x'], box['y'], box['x']+box['w'], box['y']+box['h'])))
           
           #The list of images is saved to file as a pdf
            lim[0].save(new_filepath, "PDF" ,resolution=100.0, save_all=True, append_images=lim[1:])
    
    return output_dir_l
