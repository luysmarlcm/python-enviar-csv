import csv
import requests
import time
import base64
import certifi

# Ruta del archivo CSV
csv_file_path = 'g2_v5.csv'

# URL base del endpoint (sin parámetros fijos)
api_endpoint_url = 'https://g1arcofer.815d.net:815/gateway/integracion/clientes/cuentasimple/modificar?'

# Credenciales
USERNAME = "wisphubapi"
PASSWORD = "w77SkJ9js4HD"

# Basic Auth en base64
auth_string = f"{USERNAME}:{PASSWORD}"
basic_auth_token = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

def enviar_datos_a_endpoint():
    print(f"Iniciando el envío de datos desde '{csv_file_path}' a '{api_endpoint_url}'...")

    try:
        # Aquí se realiza el cambio de codificación
        with open(csv_file_path, mode='r', encoding='latin-1') as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv, delimiter=';')
            for fila in lector_csv:
                try:
                    params = {
                        'pk': fila.get('pk'),
                        'conector': fila.get('conector'),
                        'nombre': fila.get('nombre'),
                    }
                    headers = {
                        'Authorization': f'Basic {basic_auth_token}'
                    }
                    respuesta = requests.get(api_endpoint_url, params=params, headers=headers, verify=False)
                    
                    print(f"📊 Código de estado: {respuesta.status_code}")
                    
                    # Si la API devuelve error HTTP, lanza excepción
                    respuesta.raise_for_status()

                    print("✅ Fila enviada con éxito.")

                except requests.exceptions.RequestException as e:
                    print(f"❌ Error en la solicitud: {e}")
                    print(f"No se pudo enviar la fila: {fila}")

                # Pausa opcional para no saturar el servidor
                time.sleep(1)

    except FileNotFoundError:
        print(f"❌ Error: El archivo '{csv_file_path}' no fue encontrado.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    enviar_datos_a_endpoint()
