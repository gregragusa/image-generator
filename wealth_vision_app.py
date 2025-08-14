import streamlit as st
import utils


def main():
    st.set_page_config(page_title="Wealth Vision – Batch Generator")
    st.title("Wealth Vision – Generatore batch per Ideogram")

    st.write(
        "Inserisci la tua API key Ideogram (non verrà salvata) e i prompt (uno per riga)."
    )

    api_key = st.text_input("API key Ideogram", type="password")
    prompt_text = st.text_area("Prompt (uno per riga)", height=200)

    if st.button("Genera Immagini"):
        if not api_key:
            st.warning("Inserisci la tua API key.")
            return

        prompts = [p.strip() for p in prompt_text.splitlines() if p.strip()]
        if not prompts:
            st.warning("Inserisci almeno un prompt.")
            return

        all_file_paths = []
        progress = st.progress(0.0)

        for idx, prompt in enumerate(prompts):
            st.write(f"Generazione {idx+1}/{len(prompts)} – \"{prompt}\"")
            try:
                images = utils.generate_images(api_key, prompt)
            except Exception as e:
                st.error(f"Errore per il prompt '{prompt}': {e}")
                progress.progress((idx + 1) / len(prompts))
                continue

            # Mostra le immagini e salvale
            for j, img_bytes in enumerate(images, start=1):
                st.image(img_bytes, caption=f"{prompt} – immagine {j}")
            file_paths = utils.save_images_to_temp(images, prefix=f"prompt{idx+1}")
            all_file_paths.extend(file_paths)

            progress.progress((idx + 1) / len(prompts))

        if all_file_paths:
            zip_bytes = utils.create_zip_from_files(all_file_paths)
            st.download_button(
                "Scarica tutte le immagini (ZIP)",
                data=zip_bytes,
                file_name="wealth_vision_images.zip",
                mime="application/zip",
            )
            st.success("Generazione completata!")
        else:
            st.info("Nessuna immagine generata.")


if __name__ == "__main__":
    main()
