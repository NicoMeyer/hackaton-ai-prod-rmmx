# README

Repositorio del proyecto creado para la Hackaton AI 2024 de Buk por el equipo de Remu México.

## 🤖 PR reviewer

Se desarrolló un PR reviewer basado en comentarios de los desarrolladores del equipo.

### ¿Cómo funciona?

Crear un PR y automáticamente se ejecutará una github action, que corre el script `workflow/main.py`, que revisará el código y agregará comentarios a este.

### Fine tuning y mejoras al modelo

El modelo usado para revisar los PRs es un modelo entrenado usado fine-tuning. Se entrenó el modelo gpt-4o-2024-08-06 con data de más de 3000 comentarios de PRs 🇲🇽 anteriores.

Para seguir mejorando el modelo se agregó una segunda github action que corre el script `scripts/update_jsonl_with_comments.py` cada vez que un PR es mergeado. Este script toma todos los comentarios con 👍 y 👎 y los agrega en el archivo `comments.jsonl`. Agrega la diff como input y el comentario como output, agregando si es válido o no dependiendo del thumbs. Este archivo, `comments.jsonl`, puede ser utilizado para seguir entrenando al modelo.

## Costos estimados

![Costos estimados](https://raw.githubusercontent.com/NicoMeyer/hackaton-ai-prod-rmmx/refs/heads/main/public/costos.png)

*Todos los precios están en dólares.

## 🚀 Posibles mejoras

- Automatizar el fine tuning cada cierto tiempo.
- Permitir responder los comentarios automatizados y que la IA responda a esto.
- Mayor conocimiento de la tecnología usada en Buk.
- Mayor conocimiento del negocio.
- Tener modelos especializados para distintos problemas/módulos.
- Conexión con Jira para que tenga el contexto de las tarjetas.
- Acceso a los documentos de negocio.

## 🌮🌮 Team

[paul](@paulBukDev) | [pancho](@fbarrosbuk) | [elvis](@okk-o) | [sofi](@sofiapavlovic) | [hector](@hepem) | [diego mart](@diegoamartinez) | [cusi](@gastoncusimano) | [nico](@nicomeyer) | [diego moya](@godiemp) | [rodrigo](@rgevert) | [dani](@daquiroz) | [yisus](jovalles21)
