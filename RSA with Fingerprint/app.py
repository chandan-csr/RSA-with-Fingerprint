from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import os
from minutieadetect import md
from generateprimenumbers import get_nearest_primes
from encryptimage import encrypt_image
from text import generate_keypair, ed
from textfile import encryptfile
from PIL import Image

UPLOAD_FOLDER = 'static'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def frontpage():
    return render_template('frontpage.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST','GET'])
def upload():
    global prime_before, prime_after
    if request.method == 'POST':
        file = request.files['file']
        try:
            # Delete old image
            for old_file in os.listdir('static'):
                if old_file.endswith(('.css','.ico','.jpg','.png','.mp4')):
                    continue
                os.remove(os.path.join('static', old_file))
                
            # Convert TIF image to PNG format
            if file.filename.endswith('.tif'):
                im = Image.open(file)
                file = im.convert('RGB')    
                
            #Save new image
            input_path = os.path.join('static', 'input_image.png')
            file.save(input_path)
            
            output_path = os.path.join('static', "output_image.png")
            minutiae_count = md(input_path, output_path)
            #get_nearest_primes(minutiae_count)
            prime_before, prime_after = get_nearest_primes(int(minutiae_count))
            
            return render_template('result.html', result1=url_for('static', filename='input_image.png'), result2=url_for('static', filename='output_image.png'), minutiae_count=minutiae_count, prime_before=prime_before, prime_after=prime_after)

        except Exception as e:
            #print(e)
            error_message = "Upload the Fingerprint image."
            return render_template('index.html', error= error_message)
            #return "Upload the image."
    return redirect(url_for('upload'))

@app.route('/index', methods=['GET'])
def upload_again():
    if request.method == 'GET':
        return render_template('index.html')

'''    
@app.route('/generateprime', methods=['GET'])
def generateprime():
    global prime_before, prime_after
    minutiae_count = request.args.get('minutiae_count',default=0,type=int)
    prime_before, prime_after = get_nearest_primes(int(minutiae_count))
    if prime_before is not None and prime_after is not None:
        return render_template("result.html", result1=url_for('static', filename='input_image.png'), result2=url_for('static', filename='output_image.png'), minutiae_count=minutiae_count, prime_before=prime_before, prime_after=prime_after)
    else:
        return render_template("result.html", minutiae_count=minutiae_count, error="Could not find nearest prime numbers.")
'''
       
@app.route('/process_option', methods=['POST'])
def process_option():
    selected_option = request.form['option']

    if selected_option == '1':
        return redirect(url_for('option1'))
    elif selected_option == '2':
        return redirect(url_for('option2'))
    elif selected_option == '3':
        return redirect(url_for('option3'))

@app.route('/option1')
def option1():
    return render_template('text.html')

@app.route('/option2')
def option2():
    return render_template('textfile.html')

@app.route('/option3')
def option3():
    return render_template('image.html')

@app.route('/encryptimage', methods=['POST','GET'])
def encryptimage():
    global prime_before, prime_after
    img_path = None
    if request.method == 'POST':
        file = request.files['file']
        try:
            # Delete old image
            for old_file in os.listdir('static'):
                if old_file.endswith(('.css','.ico','.gif','.svg','.webp','.png', '.mp4')):
                    continue
                os.remove(os.path.join('static', old_file))

            # Save new image in PNG format
            img = Image.open(file)
            if img.format not in ['PNG']:
                img = img.convert('RGB')
                img_path = os.path.join('static', 'encimage.png')
                img.save(img_path, 'PNG')
            else:
                img_path = os.path.join('static', 'encimage.' + img.format.lower())
                img.save(img_path)

        except Exception as e:
            print(e)
            error_message = "Upload the image to encrypt."
            return render_template('image.html', error=error_message)

    encrypt_image(prime_before, prime_after, img_path)  
    return render_template('image.html', input_image='encimage.png', output_image='enc.png', decrypted_image='dec.png')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        global plaintext
        plaintext = request.form['plaintext']
        global prime_before, prime_after
        global public_key, private_key
        global ciphertext, decryptedtext
        public_key, private_key = generate_keypair(prime_before, prime_after)
        ciphertext, decryptedtext = ed(public_key,private_key,plaintext)
        return render_template('text.html', ciphertext=ciphertext)
    return render_template('text.html')

@app.route('/decrypt', methods=['POST'])
def decrypt():
    global ciphertext, decryptedtext, plaintext
    ciphertext = request.form['ciphertext']
    global prime_before, prime_after
    global public_key, private_key
    #public, private = generate_keypair(prime_before, prime_after)
    #decryptedtext = decrypt(private_key, ciphertext)
    return render_template('text.html', plaintext=plaintext, ciphertext=ciphertext, decryptedtext=decryptedtext)

@app.route('/encrypttxtfile', methods=['POST','GET'])
def encrypttxtfile():
    global prime_after, prime_before
    global input_file_name, input_file_ext
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file and uploaded_file.filename.lower().endswith(('.txt', '.doc', '.docx','.py')):
            try:
                # Delete old file
                for old_file in os.listdir('static'):
                    if old_file.endswith(('.css','.ico','.png','.txt','.doc','.docx','.py', '.mp4')):
                        continue
                    os.remove(os.path.join('static', old_file))
                    
                # Save the uploaded file to the server
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                input_file_name, input_file_ext = os.path.splitext(file_path)
                uploaded_file.save(file_path)
                
                encryptfile(file_path,prime_before, prime_after)
                return render_template('textfile.html', encrypted_file='encrypted.txt', decrypted_file='decrypted.txt')
                
            except Exception as e:
                print(e)
                error_message = "Error encrypting file. Please try again."
                return render_template('textfile.html', error=error_message)
        else:
            error_message = "Upload a text file or word document (.txt, .doc, .docx) to encrypt."
            return render_template('textfile.html', error=error_message)
        
@app.route('/download_encrypted_file')
def download_encrypted_file():
    global input_file_name, input_file_ext
    filename = 'encrypted' + input_file_ext
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/download_decrypted_file')
def download_decrypted_file():
    global input_file_name, input_file_ext
    filename = 'decrypted' + input_file_ext
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)