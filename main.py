from flask import Flask, request, jsonify, render_template, redirect, url_for
import dotenv
import google.generativeai as genai

config = dotenv.dotenv_values(".env")
app = Flask(__name__)

API_KEY = config["API_KEY"]
DEF_INSTRUCTIONS = [
    "You are a brilliant, highly sarcastic, and witty marketing executive living in Guwahati, Assam. "
    "Your job is to create a hyper-local social media advertisement for the business name provided by the user.\n\n"
    "CRITICAL RULES:\n"
    "1. You must heavily use local context, inside jokes, and landmarks (e.g., traffic at Ganeshguri or Paltan Bazar, "
    "hanging out at Dighalipukhuri or GS Road, typical local college stereotypes, vs. Fancy Bazar bargain hunters).\n"
    "2. The advertisement must match the specific tone requested by the user.\n"
    "3. Keep the output punchy, under 120 words, structured for a social media post, and use emojis naturally.\n"
    "4. Blend English with standard local phrasing or slang seamlessly if it elevates the humor."
]
DEF_MODEL = "gemini-3.1-flash-lite"

@app.route("/")
def mn():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        try:
            # The important stuff
            bus_name=request.form.get("bus_name").strip()
            tone=request.form.get("tone").strip()
            # The optional stuff, empty if no input
            model=request.form.get("model", "").strip()
            custom_inst = request.form.get("custom_inst", "").strip()
            api_key = request.form.get("api_key", "").strip()
            # Check for falsy and use the default values
            model = model if model else DEF_MODEL
            api_key = api_key if api_key else API_KEY
    
            TEMP_DEF_INST = list(DEF_INSTRUCTIONS)
            
            if custom_inst:
                TEMP_DEF_INST.append(custom_inst)

            prompt=f"Generate using the instructions for the business named '{bus_name}' using the tone '{tone}'"

            genai.configure(api_key=api_key)

            text_model = genai.GenerativeModel(
                system_instruction=TEMP_DEF_INST,
                model_name=model
            )
            
            response = text_model.generate_content(prompt).text

            # print(response)

            return jsonify({"text": response, "success": True})
        except Exception as e:
            return jsonify({"text": str(e), "success": False})
    else:
        return redirect(url_for("mn"))
