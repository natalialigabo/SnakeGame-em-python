# 🐍 Snake Game (Python + Pygame)

Um clássico **jogo da cobrinha (Snake Game)** desenvolvido em **Python** utilizando a biblioteca **Pygame**.  
O objetivo é simples: **coma a comida, cresça e evite colidir consigo mesmo ou com as bordas da tela!**


---

## 🧩 Funcionalidades

- Movimentação suave da cobrinha usando as setas do teclado 🕹️  
- Pontuação  📊   
- Sistema de colisão com paredes e com o próprio corpo 💥  
- Interface simples e intuitiva 🧠  
- Código limpo e fácil de modificar 💻  

---


### 🧱 Pré-requisitos
Antes de começar, você precisa ter instalado em sua máquina:
- [Python 3.8+](https://www.python.org/downloads/)
- [Pygame](https://www.pygame.org/news)

---

### 🚀 Como Rodar

Para rodar o jogo, execute o seguinte comando no seu terminal:

```bash
python3 SnakeGame.py
```

**Observação:** Se você encontrar um erro `libGL error`, significa que você está em um ambiente que não tem acesso direto a um display. Para resolver isso, você pode usar um framebuffer virtual como o `Xvfb`.

1.  **Instale o Xvfb:**

    ```bash
    sudo apt-get update && sudo apt-get install -y xvfb
    ```

2.  **Rode o jogo com o Xvfb:**

    ```bash
    xvfb-run python3 SnakeGame.py
    ```
