import yaml # Primeiro precisa de instalar a biblioteca: pip3 install pyyaml

# Caminho para o seu ficheiro yaml original
yaml_file_path = 'C:\\Users\\tiago\\Desktop\\Tiago\\Moto_project\\edgetpuyolo\\data\\coco.yaml'

# Caminho para o ficheiro de labels de saída para a Jetson
output_labels_path = 'C:\\Users\\tiago\\Desktop\\Tiago\\Moto_project\\models\\coco_labels.txt'

try:
    with open(yaml_file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Extrai a lista de nomes
    class_names = data['names']
    
    # Escreve os nomes no novo ficheiro, um por linha
    with open(output_labels_path, 'w') as f:
        for name in class_names:
            f.write(f"{name}\n")
            
    print(f"Sucesso! Ficheiro '{output_labels_path}' criado com {len(class_names)} classes.")

except Exception as e:
    print(f"Ocorreu um erro: {e}")
    print("Verifique se o caminho para 'coco.yaml' está correto e se o ficheiro tem a secção 'names'.")