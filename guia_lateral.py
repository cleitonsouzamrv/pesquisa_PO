import streamlit as st

def mostrar_guia_lateral():
    st.markdown("### 🧭 Guia de Preenchimento")

    with st.container():
        st.markdown("### 1️⃣ Preencha seu e-mail")
        st.caption("Informe seu e-mail corporativo da MRV. Ele é obrigatório para validar sua resposta.")

        st.markdown("### 2️⃣ Selecione os painéis que você utiliza")
        st.caption("Você pode marcar mais de um. Escolha os que fazem parte da sua rotina.")

        st.markdown("### 3️⃣ Deixe feedbacks (opcional)")
        st.caption("Deseja sugerir melhorias ou elogiar algum painel? Clique em 'Adicionar outro feedback' para comentar mais de um.")

        st.markdown("### 4️⃣ Preencha as ferramentas utilizadas")
        st.caption("Para cada ferramenta, informe nome, objetivo, categoria, importância e horas gastas por mês.")

        st.markdown("### 5️⃣ Clique em 'Salvar e Enviar Resposta'")
        st.caption("Você verá um resumo com tudo o que foi preenchido.")

        st.markdown("### 6️⃣🚨 Faça upload das ferramentas na pasta")
        st.caption("O link da pasta está no botão 'Clique aqui' logo abaixo de 'Salvar e Enviar Resposta'")

        st.markdown("### ✅ Obrigado pela sua contribuição!")
        st.caption("Sua resposta ajuda a mapear o uso de ferramentas e painéis na equipe de Planejamento Operacional.")

