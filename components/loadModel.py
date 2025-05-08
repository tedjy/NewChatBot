# import streamlit as st
# # from llama_cpp import Llama
# # import os

# # from ctransformers import AutoModelForCausalLM
# # from transformers import AutoTokenizer
# #  Charger le modèle GGUF
# # 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
# MODEL_PATH = "./models/mistral-7b-instruct-v0.1.Q5_K_S.gguf"
# from huggingface_hub import login
# login("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")
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# from langchain.llms import HuggingFacePipeline

# def load_mistral_pipeline(model_name="mistralai/Mistral-7B-Instruct-v0.1", max_new_tokens=512):
#     tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
#     model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")

#     pipe = pipeline(
#         "text-generation",
#         model=model,
#         tokenizer=tokenizer,
#         max_new_tokens=max_new_tokens,
#         do_sample=True,
#         top_p=0.9,
#         temperature=0.7
#     )

#     return HuggingFacePipeline(pipeline=pipe)
    