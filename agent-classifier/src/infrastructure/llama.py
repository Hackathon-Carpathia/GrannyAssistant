from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from transformers import BitsAndBytesConfig
import json

def get_quantization_config():
    return BitsAndBytesConfig(
        load_in_8bit=True,
        bnb_8bit_quant_type='nf8',
        bnb_8bit_use_double_quant=True,
        bnb_8bit_compute_dtype=torch.bfloat16
    )

def load_model_and_tokenizer(model_name: str):
    quantization_config = get_quantization_config()

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=quantization_config,
        num_labels=5,
        device_map='auto'
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name, add_prefix_space=True)
    tokenizer.pad_token_id = tokenizer.eos_token_id
    tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer

def prepare_prompt():
    return """
    Odpowiadaj wyłącznie JSON. Jeśli sytuacja jest krytyczna ('emergency'),
    podaj jedno zwięzłe zdanie opisujące zagrożenie Basi opisane prompcie wejściowym (w trzeciej osobie)
    oraz zalecenie rozważenia pomocy medycznej jako 'Powód decyzji'. Jeśli sytuacja nie jest nagła ('rozmowa'),
    zwróć 'OCENA SYTUACJI': 'rozmowa' oraz pustą 'Powód decyzji'. Przykład:
    input: "Pomocy, spadłam ze schodów! Ból w nodze jest nie do wytrzymania!"
    {
        "OCENA SYTUACJI": "emergency",
        "Powód decyzji": "Basia doznala wypadku i urazu nogi, co może wymagać pomocy. Skontaktuj się z nią!"
    }
    "Powód decyzji" musi być mniej niż 140 znaków!
    """

def generate_response(user_input):
    messages.append({"role": "user", "content": user_input})
    formatted_input = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
    inputs = tokenizer(formatted_input, return_tensors="pt").to(model.device)
    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]
    outputs = model.generate(
        inputs['input_ids'],
        max_new_tokens=120,
        eos_token_id=terminators,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        temperature=0.9,
        top_p=0.6,
    )
    response = outputs[0][inputs['input_ids'].shape[-1]:]
    decoded_response = tokenizer.decode(response, skip_special_tokens=False)
    messages.append({"role": "assistant", "content": decoded_response})
    return decoded_response


def parse_response(response_str: str):
    while True:
        try:
            print(response_str)
            response_str_cleaned = response_str.replace("<|eot_id|>", "").strip().strip("`")
            print(response_str_cleaned)
            response_dict = json.loads(response_str_cleaned)

            ocena_sytuacji = response_dict.get("OCENA SYTUACJI")
            powod_decyzji = response_dict.get("Powód decyzji")
            if len(powod_decyzji) > 160:
                messages.append({"role": "system", "content": "Wygenerowana wiadomosc za dluga - skróć ją"})
                continue
            return ocena_sytuacji, powod_decyzji

        except json.JSONDecodeError:
            messages.append({"role": "system", "content": """Nieprawidłowo wygenorowany JSON. Wygeneruj poprawny JSON. Przyklad          ```
         {
           "OCENA SYTUACJI": "rozmowa"
           "Powód decyzji": ""
         }
         ```"""})

            continue

model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
model, tokenizer = load_model_and_tokenizer(model_name)
system_prompt = prepare_prompt()
messages = [
    {"role": "system", "content": prepare_prompt()},
]

if __name__ == "__main__":
    user_input = "Pomocy, chyba mam zawał! Ten ból w klatce piersiowej jest nie do wytrzymania!"
    response = generate_response(model, tokenizer, system_prompt, user_input)
    print(response)