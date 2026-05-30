from google import genai
from google.genai import types, errors
from flask import Flask, request, jsonify, url_for, redirect, render_template
import dotenv

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
def main():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit_route():
    if request.method == "POST":
        try:
            # The important stuff
            bus_name = request.form.get("bus_name").strip()
            tone = request.form.get("tone").strip()
            # The optional stuff, empty if no input
            model = request.form.get("model", "").strip()
            custom_inst = request.form.get("custom_inst", "").strip()
            api_key = request.form.get("api_key", "").strip()
            # Check for falsy and use the default values
            model = model if model else DEF_MODEL
            api_key = api_key if api_key else API_KEY

            # add custom instructions to the main instructions if any, or else just pass in the default instructions according to the project
            TEMP_DEF_INST = list(DEF_INSTRUCTIONS)

            if custom_inst:
                TEMP_DEF_INST.append(custom_inst)

            prompt = f"Generate using the instructions for the business named '{bus_name}' using the tone '{tone}'"
            # First initialize the clietn with the api key

            with genai.Client(api_key=api_key) as client:
                # Next add configurations for the generate content model
                config = types.GenerateContentConfig(
                    system_instruction=TEMP_DEF_INST, temperature=0.7
                )

                res = client.models.generate_content(
                    model=model, contents=prompt, config=config
                )

                response = res.text

            return jsonify({"text": response, "success": True})
        except errors.ClientError as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                return (
                    jsonify(
                        {
                            "text": "Rate limited reached, please change model or use Custom API key",
                            "success": False,
                            "ratelimit": True,
                        }
                    ),
                    429,
                )
            return jsonify(
                {"text": f"An unknown exception occured {err}", "success": False}
            )
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                return (
                    jsonify(
                        {
                            "success": False,
                            "ratelimit": True,
                            "text": "Rate limit reached! ⏳ Please open 'Engine Config' in the top right corner and swap to a different fallback engine.",
                        }
                    ),
                    429,
                )
            return jsonify({"text": str(e), "success": False})
    else:
        return redirect(url_for("main"))
