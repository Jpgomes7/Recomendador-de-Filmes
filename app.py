import streamlit as st
from recomendador import dados, recomendar_detalhado

st.set_page_config(page_title='CineMatch', page_icon='🎬', layout='wide')

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero { padding: 1.2rem 0 0.4rem 0; }
.eyebrow {
    color: #E3B23C; font-weight: 700; letter-spacing: 0.18em;
    font-size: 0.78rem; text-transform: uppercase;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif; font-size: 4.2rem;
    color: #F1EDE3; line-height: 1; margin: 0.2rem 0 0.4rem 0;
}
.hero-sub { color: #9A9FB0; font-size: 1rem; max-width: 560px; margin-bottom: 0.6rem; }
.marquee { letter-spacing: 6px; color: #E3B23C; opacity: 0.55; font-size: 0.7rem; margin-bottom: 1.4rem; }

.sidebar-title {
    font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem;
    color: #E3B23C; letter-spacing: 0.05em; margin-bottom: 0.6rem;
}

.ticket {
    position: relative; background: #1C1F2B; border-radius: 14px;
    border: 1px solid rgba(227,178,60,0.25); overflow: hidden; margin-bottom: 1.1rem;
}
.ticket-notch {
    position: absolute; width: 18px; height: 18px; background: #0E1018;
    border-radius: 50%; right: 92px;
}
.ticket-notch.top { top: -9px; }
.ticket-notch.bottom { bottom: -9px; }
.ticket-inner { display: flex; }
.ticket-main { flex: 1; padding: 1.1rem 1.2rem; }
.ticket-rank { color: #E3B23C; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.1em; }
.ticket-title {
    font-family: 'Bebas Neue', sans-serif; font-size: 1.7rem; color: #F1EDE3;
    line-height: 1.1; margin: 0.15rem 0 0.5rem 0;
}
.pill {
    display: inline-block; background: rgba(227,178,60,0.12); color: #E3B23C;
    border: 1px solid rgba(227,178,60,0.3); border-radius: 999px;
    padding: 0.15rem 0.65rem; font-size: 0.72rem; margin: 0 0.3rem 0.3rem 0;
}
.ticket-stub {
    width: 92px; border-left: 2px dashed rgba(227,178,60,0.4);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 0.15rem; padding: 0.5rem;
}
.stub-pct { font-family: 'Bebas Neue', sans-serif; font-size: 1.6rem; color: #E3B23C; }
.stub-label { color: #9A9FB0; font-size: 0.62rem; letter-spacing: 0.1em; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="eyebrow">🎬 Sessão contínua</div>
    <div class="hero-title">CineMatch</div>
    <div class="hero-sub">Escolha um filme que você já gosta e descubra outros parecidos, com base em sinopse, gêneros, elenco e diretor.</div>
    <div class="marquee">● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-title">🎟️ Controles</div>', unsafe_allow_html=True)
titulos = sorted(dados['title'].unique())
titulo_escolhido = st.sidebar.selectbox('Filme de referência', titulos)
quantidade = st.sidebar.slider('Quantas recomendações?', min_value=3, max_value=10, value=6)
gerar = st.sidebar.button('Gerar recomendações', use_container_width=True)

if gerar:
    recomendacoes = recomendar_detalhado(titulo_escolhido, quantidade)
    st.subheader(f'Parecidos com "{titulo_escolhido}"')
    colunas = st.columns(2)
    for posicao, filme in enumerate(recomendacoes):
        pct = round(filme['similaridade'] * 100)
        pills = ''.join(f'<span class="pill">{genero}</span>' for genero in filme['generos'][:3])
        colunas[posicao % 2].markdown(f"""
        <div class="ticket">
            <div class="ticket-notch top"></div>
            <div class="ticket-notch bottom"></div>
            <div class="ticket-inner">
                <div class="ticket-main">
                    <div class="ticket-rank">Nº {posicao + 1:02d}</div>
                    <div class="ticket-title">{filme['titulo']}</div>
                    <div>{pills}</div>
                </div>
                <div class="ticket-stub">
                    <div class="stub-pct">{pct}%</div>
                    <div class="stub-label">match</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)