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

> **Créditos:** Modelos de planetas e assets adaptados (Purple Planet por Yo.Ri e Green Planet por jimmyn64, CC BY 4.0).
