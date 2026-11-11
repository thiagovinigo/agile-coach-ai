# 🪐 Catálogo de Modelos 3D GLB (Star Wars & Planetas)

Este kit disponibiliza **6 modelos 3D de alta fidelidade** em formato binário `.glb` otimizados para WebGL, Three.js, Spline e Babylon.js.

---

## 🚀 Modelos Inclusos no Projeto

| Modelo 3D | Arquivo | Tamanho | Uso Recomendado |
| :--- | :--- | :--- | :--- |
| **Estrela da Morte** | `slides-3d/app/assets/death-star.glb` | 18.3 MB | Cenas de ameaça, escala colossal, estação espacial orbital |
| **Jedi Starfighter** | `slides-3d/app/assets/jedi-starfighter.glb` | 30.2 MB | Nave de interceptação, velocidade, combate ágil, foco em primeiro plano |
| **Millennium Falcon** | `slides-3d/app/assets/millennium-falcon.glb` | 1.75 MB | Nave icônica, manobras de fuga, hiperespaço, elemento central da narrativa |
| **Base de Naboo** | `slides-3d/app/assets/naboo-base.glb` | 43.5 MB | Cenário planetário, arquitetura clássica, ambiente majestoso e luminoso |
| **Base de Tatooine** | `slides-3d/app/assets/tatooine-base.glb` | 23.2 MB | Cenário desértico, posto avançado, sol duplo, atmosfera áspera |
| **Imperial TIE Fighter** | `slides-3d/app/assets/tie-fighter.glb` | 6.64 MB | Patrulha hostil, caça imperial, enxame inimigo em profundidade |

---

## 🛠️ Como Carregar em Qualquer Projeto Three.js

```javascript
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const loader = new GLTFLoader();

// Exemplo: Carregando a Millennium Falcon
loader.load('slides-3d/app/assets/millennium-falcon.glb', (gltf) => {
    const model = gltf.scene;
    model.scale.set(1.5, 1.5, 1.5);
    model.position.set(0, 0, -10);
    scene.add(model);
    
    // Animação de rotação contínua
    function animate() {
        requestAnimationFrame(animate);
        model.rotation.y += 0.005;
    }
    animate();
});
```

> **Créditos:** Modelos de planetas e assets adaptados do [Sketchfab](https://sketchfab.com/) (Purple Planet por Yo.Ri e Green Planet por jimmyn64, CC BY 4.0).

---

## 🌐 Onde Encontrar Novos Modelos e Referências de Design

### 1. Sketchfab (sketchfab.com) — Repositório de Modelos 3D GLB
O **[Sketchfab](https://sketchfab.com/)** é a principal fonte global de modelos 3D em tempo real para WebGL:
- **Filtro Recomendado:** Busque pelo tema (ex: `spaceship`, `drone`, `cyberpunk city`, `gadget`), ative o filtro **Downloadable** e selecione licenças **CC Attribution**.
- **Formato:** Baixe sempre a opção **glTF / GLB** (formato binário com geometria, materiais e texturas embutidos em um único arquivo).
- **Inspeção Prévia:** Use o visualizador 3D do Sketchfab e aperte `5` ou acesse o menu de Wireframe para inspecionar a contagem de polígonos (ideal: menos de 80.000 triângulos para apresentações web a 60 FPS).
- **Sketchfab Viewer API:** Se preferir não hospedar o arquivo `.glb`, você pode incorporar o modelo diretamente no slide usando a [Sketchfab Viewer API](https://sketchfab.com/developers/viewer) e controlar animações e câmeras via JavaScript.

### 2. Behance (behance.net) — Direção de Arte & Apresentações Visuais
O **[Behance](https://www.behance.net/)** é a referência máxima para direção de arte, composição editorial e slides de estúdio:
- **Pesquisas Recomendadas:** `Presentation Design`, `Keynote Presentation`, `Pitch Deck 3D`, `Kinetic Typography`, `Brand Identity Deck`.
- **O que observar:** Relação de escala entre números monumentais e legendas pequenas, paletas restritas (máximo 3 cores dominantes), ritmo de respiração visual e grids assimétricos.
- **Aplicação no Deck:** Use o Behance para montar o *moodboard* na Pergunta 8/10 (Identidade Visual) e desenhar layouts autorais que escapam do padrão genérico de 3 cards corporativos.
