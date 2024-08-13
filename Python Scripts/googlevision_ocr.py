import os
import json
import glob
from google.cloud import vision 
from google.cloud import storage


#Path of the directory where the files to be OCRed are located.
input_dir='...'
#Path of the directory where you will want the output text files to be stored.
output_dir='...'
#Name of your Google Cloud Storage Bucket.
bucket_name='...'
#Location of Google Service Account Key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="..."

#Instantiate a client for the client libraries 'storage' and 'vision', and the services which you want to use, i.e. the DOCUMENT_TEXT_DETECTION of the ImageAnnotator service, incr. batch size if merge operation fails and manual extract. is required
storage_client = storage.Client()
vision_client = vision.ImageAnnotatorClient()
bucket = storage_client.get_bucket(bucket_name)
feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
#The number of pages which will be grouped in each json response file - keep @ 2 for efficiency/cost-effectiveness esp. for double-page scans
batch_size = 2
#The file format used (the alternative is 'image/tiff' if you are working with .tiff image files instead of pdfs).
mime_type = 'application/pdf'


def batch_OCR_local_dir(input_dir, output_dir):

#If the output directory does not already exist, create it
    if not os.path.exists(output_dir): 
         os.mkdir(output_dir)

#Iterate through filenames in local directory
    for filename in os.listdir(input_dir): 
        if filename.endswith('.pdf'):
            print(filename)

            #Create a remote path. The combination of os.path.basename and os.path.normpath extracts the name of the last directory of the path, i.e. 'docs_to_OCR'. Using the full path would create many useless nested directories inside your bucket.
            remote_subdir= os.path.basename(os.path.normpath(input_dir))
            rel_remote_path = os.path.join(remote_subdir, filename)
            #upload file to your Google Cloud Bucket as a blob
            blob = bucket.blob(rel_remote_path)
            blob.upload_from_filename(os.path.join(input_dir, filename))

            #Path to the file
            gcs_source_uri = os.path.join('gs://', bucket_name, rel_remote_path)

            #Input source and input configuration
            gcs_source = vision.GcsSource(uri=gcs_source_uri)
            input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

            #Path to the response JSON files in the Google Cloud Storage. In this case, the JSON files will be saved inside a subfolder of the Cloud version of the input_dir called 'json_output'.
            gcs_destination_uri = os.path.join('gs://', bucket_name, remote_subdir, 'json_output', filename[:30]+'_')
           
            #Output destination and output configuration
            gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
            output_config = vision.OutputConfig(gcs_destination=gcs_destination, batch_size=batch_size)
        
            #Instantiate OCR annotation request, inc. timeout if >500mb
            async_request = vision.AsyncAnnotateFileRequest(features=[feature], input_config=input_config, output_config=output_config)
            operation = vision_client.async_batch_annotate_files(requests=[async_request])
            operation.result(timeout=360) #reset to 180 if issue

            #Identify the 'prefix' of the response JSON files, i.e. their path and the beginning of their filename
            prefix='/'.join(gcs_destination_uri.split('//')[1].split('/')[1:])

            #Use this prefix to extract the correct JSON response files from your bucket and store them as 'blobs' in a list. The term 'blob' stands for 'Binary Large Object' and is used for storing information.
            blob_list = list(bucket.list_blobs(prefix=prefix))

            #Order the list by length before sorting it alphabetically so that the text appears in the correct order in the output file (i.e. so that the first two items of the list are 'output-1-to-2.json' and 'output-2-to-3.json' instead 'output-1-to-2.json' and 'output-10-to-11.json', as produced by the default alphabetical order).
            blob_list = sorted(blob_list, key=lambda blob: 
                len(blob.name))

            #Create an empty string to store the text
            output = ''

            #For each JSON file, extract the full text annotations and add them to the output string
            for blob in blob_list:
                print((blob.name).split('/')[-1:][0])
                json_string = blob.download_as_string()
                response=json.loads(json_string)
                full_text_response = response['responses']

                for text in full_text_response:
                    try:
                        annotation=text['fullTextAnnotation']
                        output+=annotation['text']
                    except:
                        pass

            #Create the path and name of the output file
            output_file=os.path.join(output_dir, filename.split('.')[0]+'.txt')

            #Create a file and write the output string
            f=open(output_file, 'x')
            f.write(output)
            f.close()

#execute the function
batch_OCR_local_dir(input_dir, output_dir)
