const fs = require('fs');
const path = require('path');
const vm = require('vm');

// Pega a chave da API pelas variáveis de ambiente
const apiKey = process.env.OPENAI_API_KEY;
if (!apiKey) {
    console.error("=========================================");
    console.error("ERRO: Chave da OpenAI não encontrada!");
    console.error("Execute o script passando a chave, exemplo no CMD/PowerShell:");
    console.error("$env:OPENAI_API_KEY=\"sk-sua-chave-aqui\"; node generate_images_openai.js");
    console.error("=========================================");
    process.exit(1);
}

const imagesDir = path.join(__dirname, 'images');
if (!fs.existsSync(imagesDir)) fs.mkdirSync(imagesDir);

async function generateImage(title, detail) {
    // Prompt focado em ilustração flat realista, vibrante e corporativa
    const prompt = `A realistic, high-quality flat illustration for an agile team technique called '${title}'. Concept: ${detail}. Clean, modern corporate aesthetic. Vibrant colors, flat vector UI design style. No text or typography.`;
    
    console.log(`\nGerando: ${title}...`);
    
    const response = await fetch('https://api.openai.com/v1/images/generations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            model: "dall-e-2",
            prompt: prompt,
            n: 1,
            size: "1024x1024"
        })
    });

    if (!response.ok) {
        const err = await response.text();
        throw new Error(`OpenAI API error: ${err}`);
    }

    const data = await response.json();
    return data.data[0].url;
}

async function processFile(filename, variableName) {
    console.log(`\n--- Processando ${filename} ---`);
    const code = fs.readFileSync(filename, 'utf8');
    
    // Executa o código JS do arquivo para extrair o objeto
    const sandbox = {};
    vm.createContext(sandbox);
    
    // Converte const para var ou anexa ao sandbox para podermos ler
    const executableCode = code + `\nthis.exportedData = ${variableName};`;
    vm.runInContext(executableCode, sandbox);
    
    const dataObj = sandbox.exportedData;

    for (const category in dataObj) {
        const items = dataObj[category];
        for (let i = 0; i < items.length; i++) {
            const item = items[i];
            
            // Verifica se já geramos uma imagem para esse item
            if (item.board_html && item.board_html.includes('<img src="images/')) {
                console.log(`[PULADO] ${item.title} (Já possui imagem)`);
                continue;
            }

            let retries = 0;
            let success = false;
            while (!success && retries < 3) {
                try {
                    // Gera a URL da imagem na OpenAI
                    const url = await generateImage(item.title, item.detail);
                    
                    const imageName = item.title.replace(/[^a-z0-9]/gi, '_').toLowerCase() + '.jpg';
                    const imagePath = path.join(imagesDir, imageName);
                    
                    // Faz o download da imagem e salva na pasta images/
                    console.log(`Baixando imagem para ${imagePath}...`);
                    const res = await fetch(url);
                    const buffer = await res.arrayBuffer();
                    fs.writeFileSync(imagePath, Buffer.from(buffer));

                    // Atualiza o HTML para usar a imagem salva
                    item.board_html = `<div style="text-align: center;"><img src="images/${imageName}" alt="${item.title}" style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>`;
                    
                    // Salva o arquivo imediatamente para não perder o progresso se der erro na próxima
                    const newCode = `const ${variableName} = ` + JSON.stringify(dataObj, null, 4) + `;\n`;
                    fs.writeFileSync(filename, newCode, 'utf8');
                    console.log(`[SUCESSO] ${item.title} salvo!`);
                    
                    success = true;
                    // Pausa 12 segundos para não estourar o limite de 5 img/min da OpenAI (Tier 1)
                    await new Promise(r => setTimeout(r, 12000));
                    
                } catch (err) {
                    console.error(`[ERRO] Tentativa ${retries+1} falhou para ${item.title}: ${err.message}`);
                    retries++;
                    if (retries < 3) {
                        console.log("Pausando por 20 segundos antes de tentar novamente...");
                        await new Promise(r => setTimeout(r, 20000));
                    } else {
                        console.log("Desistindo desse item após 3 tentativas.");
                    }
                }
            }
        }
    }
}

async function run() {
    console.log("Iniciando geração de imagens com DALL-E 3 (OpenAI)...");
    await processFile('facilitador_dinamicas_data.js', 'facilitadorDinamicasData');
    await processFile('tecnicas_facilitacao_data.js', 'tecnicasFacilitacaoData');
    console.log("\nProcesso 100% finalizado!");
}

run();
