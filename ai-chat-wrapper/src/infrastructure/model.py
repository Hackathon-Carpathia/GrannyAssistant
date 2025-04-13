import openai
import json
from openai import OpenAI

client = OpenAI(
    api_key="")
system_prompt = """
Nazywasz się Halina. Jesteś asystentem osoby starszej, pani Barbary, zwracaj się do niej Basiu.
Wiadomości pochodzą z rozpoznawania mowy i mogą zawierać błędy, nawet zmieniające znaczenie zdania (np. niepoprawne rozpoznanie przeczenia).
W przypadku wątpliwości, kiedy może być konieczność udzielenia pomocy, zawsze zakładaj, że taka konieczność jest.
Generuj wyjście w formacie JSON.
Wejścia również dostajesz w postaci JSON, w polu "message" podaj wiadomość do osoby, w opcjonalnym polu "memory" (typ text) możesz zawrzeć wiadomość do umieszczenia w pamięci, jeśli uznasz, że dana informacja może przydać się w dalszej przyszłości.
Dzisiejsza data: 2025-04-12.
Zapisuj w pamięci również informacje o istotnych zdarzeniach razem z datą.
Są jeszcze opcjonalne pola "emergency_message" dla służb ratunkowych i "guardian_message" dla opiekuna (typ text). Nie używaj ich bez potrzeby.
"""
memory = ""
def send_message(input_dict):
    global memory
    messages.append({"role": "user", "content": json.dumps(input_dict)})
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3
    )
    output = response.choices[0].message.content.strip()

    try:
        output_dict = json.loads(output)
        allowed_keys = {"message"}
        memory+= output_dict["memory"] if "memory" in output_dict.keys() else ""
        cleaned_output = {key: output_dict[key] for key in allowed_keys if key in output_dict}
        return cleaned_output

    except json.JSONDecodeError:
        print("Błąd: Niepoprawna odpowiedź JSON od modelu!")
        return None

messages = [
    {"role": "system", "content": system_prompt + "memory \n" + memory},
]
# Przykład użycia
if __name__ == "__main__":
    # wejscie = {
    #     "userprompt": "duuuuzo lepiej. co u moich wnukow ciekawe"
    # }
    wejscie = {"reminderprompt": "Przypomnij o serialu "}
    odpowiedz = send_message(wejscie)
    print(json.dumps(odpowiedz, indent=2, ensure_ascii=False))