import streamlit as st
import utils

AR_PRESETS = {
    "Quadrato (1:1)": "1x1",
    "Orizzontale 16:9": "16x9",
    "Verticale 9:16 (stories)": "9x16",
    "Orizzontale 4:3": "4x3",
}

def main():
    st.set_page_config(page_title="Wealth Vision – Batch Generator")
    st.title("Wealth Vision – Generatore batch per Ideogram")

    st.write("Inserisci la tua API key Ideogram e i prompt (uno per riga). "
             "Scegli il formato e scarica direttamente lo ZIP (le anteprime non vengono mostrate).")

    api_key = st.text_input("API key Ideogram", type="password")
    aspect_choice = st.selectbox("Formato immagine (aspect ratio)", list(AR_PRESETS.keys()), index=0)
    num_images = st.number_input("Numero di immagini per prompt", min_value=1, max_value=8, value=1, step=1)
    rendering_speed = st.selectbox("Qualità/Velocità", ["DEFAULT", "TURBO", "QUALITY"], index=0)

    prompt_text = st.text_area("Prompt (uno per riga)", height=200,
                               placeholder="Prompt 1\nPrompt 2\nPrompt 3")

    if st.button("Genera e scarica ZIP"):
        if not api_key:
            st.warning("Inserisci la tua API key.")
            return

        prompts = [p.strip() for p in prompt_text.splitlines() if p.strip()]
        if not prompts:
            st.warning("Inserisci almeno un prompt.")
            return

        ar_value = AR_PRESETS[aspect_choice]
        all_file_paths = []
        progress = st.progress(0.0)

        for idx, prompt in enumerate(prompts, start=1):
            try:
                images = utils.generate_images(
                    api_key=api_key,
                    prompt=prompt,
                    aspect_ratio=ar_value,          # << usa l’aspect ratio scelto
                    num_images=num_images,
                    rendering_speed=rendering_speed,
                    # niente preview: solo salvataggio+zip
                )
            except Exception as e:
                st.error(f"Errore con il prompt {idx}: {e}")
                progress.progress(idx / len(prompts))
                continue

            # salva in temp ma non mostra le immagini
            file_paths = utils.save_images_to_temp(images, prefix=f"p{idx}")
            all_file_paths.extend(file_paths)
            progress.progress(idx / len(prompts))

        if all_file_paths:
            zip_bytes = utils.create_zip_from_files(all_file_paths)
            st.download_button(
                "Scarica immagini (ZIP)",
                data=zip_bytes,
                file_name="wealth_vision_images.zip",
                mime="application/zip",
            )
            st.success("ZIP pronto!")
        else:
            st.info("Nessuna immagine generata.")

if __name__ == "__main__":
    main()
