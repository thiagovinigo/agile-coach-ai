export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    try {
        const { messages, systemPrompt } = req.body;
        
        if (!messages || !Array.isArray(messages)) {
            return res.status(400).json({ error: 'Messages array is required' });
        }

        const apiKey = process.env.OPENAI_API_KEY;
        
        if (!apiKey) {
            return res.status(500).json({ 
                error: 'OPENAI_API_KEY não configurada no servidor (Vercel).' 
            });
        }

        // Construir o array de mensagens
        const apiMessages = [];
        if (systemPrompt) {
            apiMessages.push({ role: 'system', content: systemPrompt });
        }
        apiMessages.push(...messages);

        // Fazer a chamada para a OpenAI
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: 'gpt-4o', // ou gpt-3.5-turbo
                messages: apiMessages,
                temperature: 0.7,
                max_tokens: 1000
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error?.message || 'Erro na API da OpenAI');
        }

        return res.status(200).json({
            reply: data.choices[0].message.content
        });

    } catch (error) {
        console.error('Chat API Error:', error);
        return res.status(500).json({ error: error.message });
    }
}
