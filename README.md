# Detector de Cáncer de Piel con TensorFlow

Este proyecto utiliza TensorFlow para construir un modelo de aprendizaje profundo que detecta el cáncer de piel a partir de imágenes. El modelo está entrenado para clasificar imágenes de lesiones cutáneas como benignas o malignas.

## Características del Proyecto

- **Preprocesamiento de Datos**: Utiliza `ImageDataGenerator` para la augmentación de datos y la normalización.
- **Arquitectura del Modelo**: Una red neuronal convolucional (CNN) con múltiples capas de convolución y pooling.
- **Entrenamiento del Modelo**: Entrenado con un conjunto de datos de imágenes de lesiones cutáneas, utilizando técnicas de ajuste de pesos de clase para manejar el desbalance de clases.
- **Evaluación del Modelo**: Evaluado en un conjunto de datos de validación para medir su precisión y pérdida.
- **Guardado del Modelo**: El modelo entrenado se guarda en un archivo `.keras` para su uso futuro.

## Requisitos

- Python 3.x
- TensorFlow 2.x
- Un conjunto de datos de imágenes de lesiones cutáneas

## Instalación

1. Clona este repositorio:
    ``Se puede usar git para clonar de GTHUB o directamente el zip Grupo3_IA_CancerPiel

2. Instala las dependencias:
    ```bash
    pip install tensorflow
    ```

3. Coloca tu conjunto de datos en la carpeta `train` con la siguiente estructura:
    ```
    train/
    ├── benign/
    │   ├── imagen1.jpg
    │   ├── imagen2.jpg
    │   └── ...
    └── malignant/
        ├── imagen1.jpg
        ├── imagen2.jpg
        └── ...
    ```

## Uso

1. Ejecuta el script de entrenamiento:
    ```bash
    jupyter notebook MVP.ipynb
    ```

2. El modelo entrenado se guardará como [`modelo_cancer_piel.keras`]


## Pruebas

1. Ejecuta el script de Test:
    ```bash
    jupyter notebook Test_Model.ipynb
    ```
2. Cambia las rutas de imagenes y ejecuta
   ```bash
    image_path = r'tu/ruta/de/pruba'
    ```
3. Imagenes de prueba:
   ''En la carpeta pruebas
   

