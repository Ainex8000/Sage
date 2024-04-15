# Import our libs
import os
# Import our libs for the GUI tkinter
import tkinter as tk
# Import our libs to create a textarea with a scrollbar
from tkinter import scrolledtext
# Import our lib to load our language model and generate responses
from llama_cpp import Llama
# Import our rand lib to generate random numbers
import random
# Import a lib to get the current date
import datetime

# Create a global variable for the path to our model
# If you use a different later, you need to change this path
########## This is where you need to change the path to your model ##########
model_path = "llama-2-7b-chat.Q5_K_M.gguf"

# Create a global variable to set the version of your application
version = "1.00"

# Get the current date and stuff into a variable
todays_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Create function to load our model
def load_model():
    # Check if the model path is valid
    if not os.path.isfile(model_path):
        print("ERROR: The model path is not valid!, please check the path in the main.py file")
        print("Make sure the model is in the same directory as main.py.")
        # If the model path is not valid, exit the program
        exit()

    # If the mode path is valid, load the model
    global model
    model = Llama(
        model_path=model_path,
        seed=random.randint(1, 2**31)
    )

# Create function to generate a response
def generate_response(model, input_tokens, prompt_input_text):
    # Display the input text in the textarea response on top
    text_area_display.insert(tk.INSERT, '\n\nUser: ' + prompt_input_text + '\n')

    output_response_text = b""
    count = 0
    output_response_text = b"\n\nSage: "
    text_area_display.insert(tk.INSERT, output_response_text)
    # Generate a response
    for token in model.generate(input_tokens, top_k=40, top_p=0.95, temp=0.72, repeat_penalty=1.1):
        # Extract the response text from the output of the model which is in token 
        # format and convert it to a string
        response_text = model.detokenize([token])
        output_response_text = response_text.decode()
        # Display the response text in the textarea response on top
        text_area_display.insert(tk.INSERT, output_response_text)
        root.update_idletasks()
        count += 1
        # Now that we have a response, we can break out of the loop
        if count > 2000 or (token == model.token_eos()): 
            break
        # And we can clear in the input to let the user know the response
        # from the model is complete
        text_area_main_user_input.delete('1.0', 'end')

# Create a function to send a message to the model and display a response
def send_message():
    # Get the text from the textarea input that the user typed in.
    user_prompt_input_text = text_area_main_user_input.get('1.0', 'end-1c')
    # Delete any leading or trailing spaces from the user input.
    user_prompt_input_text = user_prompt_input_text.strip()
    # ecode the message with uft-8
    byte_message = user_prompt_input_text.encode('utf-8')

    # Create a variable to hold a personality description for our AI
    ai_personality = """You are to take on the persona of a grandmother.
    You are to be kind and understanding. 
    You are to be a baker who loves sharing sweets with her grandchildren. 
    You are to treat the user as a grandchild. 
    You are to be a loving and caring. 
    You are to be a good listener and offer advice when asked.
    """

    
    # Encode this as byte string
    byte_ai_personality = ai_personality.encode('utf-8')

    # Here is where you can change the prompt format for the LLM.
    # This is something you will need to experiment with to get the best results.
    input_tokens = model.tokenize(b"### Human: " + byte_message + b"\n### Assistant: ")

    # print out the input tokens to the console for debugging and information on how this works.
    print("Input tokens: ", input_tokens)

    # Call the generate_response function to generate a response
    generate_response(model, input_tokens, user_prompt_input_text)

# Our main function to build the GUI
def main():
    # Load our model when our app starts!
    load_model()
    # Create our GUI
    # Remember root is in this case our main window
    global root
    root =tk.Tk()

    # Set the title of our app
    root.title("Hal9000 -v" + version + " - " + todays_date)
    # Create a frame to add a scrollbar to our textarea
    frame_display = tk.Frame(root)
    scrollbar_frame_display = tk.Scrollbar(frame_display)
    # The text area where we will display the response from the model plus the user input together
    # This will allows to see the conversation history between the user and the model in one place
    global text_area_display
    text_area_display = scrolledtext.ScrolledText(frame_display, height=25, width=128, yscrollcommand=scrollbar_frame_display.set)
    # Create our colors here. You can change these to whatever you want.
    my_light_yellow = "#ffff33"
    my_dark_grey = "#202020"
    # Set the background and foreground colors of the textarea, and font. Change these to whatever you want.
    text_area_display.config(background=my_dark_grey, foreground=my_light_yellow, font=("Courier", 12))
    scrollbar_frame_display.config(command=text_area_display.yview)
    text_area_display.pack(side=tk.LEFT,fill=tk.BOTH)
    scrollbar_frame_display.pack(side=tk.RIGHT, fill=tk.Y)
    # Fill our root window with the frame
    frame_display.pack()

    frame_controls = tk.Frame(root)
    # Create a label to let the user know what LLM model and path to the model we are currently using
    model_path_label = tk.Label(frame_controls, text="Model Path: " + model_path, font=("Courier", 12))
    model_path_label.pack(side=tk.LEFT, padx=10)
    frame_controls.pack(fill=tk.BOTH, padx=5, pady=5)

    # Create our fram for the user input, remember this is at the bottom of our app
    frame_user_input = tk.Frame(root)
    frame_user_input.pack(fill=tk.BOTH)

    frame_main_user_input = tk.Frame(root)
    scrollbar_main_user_input = tk.Scrollbar(frame_main_user_input)

    global text_area_main_user_input
    text_area_main_user_input = scrolledtext.ScrolledText(frame_main_user_input, height=5, width=128, yscrollcommand=scrollbar_main_user_input.set)
    # Set the background and foreground colors of the textarea, and font. Change these to whatever you want.
    text_area_main_user_input.config(background=my_dark_grey, foreground=my_light_yellow, font=("Courier", 12))
    scrollbar_main_user_input.config(command=text_area_main_user_input.yview)
    # Fill our root window with the frame
    text_area_main_user_input.pack(side=tk.LEFT,fill=tk.BOTH)
    scrollbar_main_user_input.pack(side=tk.RIGHT, fill=tk.Y)
    frame_main_user_input.pack()

    # Create a button to send the user input to the model 
    # Remember the enter key will NOT send the user input to the model. You must press the button! However, you can change this.
    send_button = tk.Button(root, text="Send", command=send_message)
    # Fill our root window with the button
    send_button.pack()
    # Must have this to run our app
    root.mainloop()

# App start here
if __name__ == "__main__":
    # Call our main function to start the app!
    main()
