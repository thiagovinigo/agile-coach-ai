# Passo 5: Colunas, Split e WIP Limits

Agora que os "States" existem no banco de dados, precisamos desenhar o tabuleiro onde as pessoas vão trabalhar: o Kanban Board. E vamos mapear cada Coluna do Board para um State que criamos no Passo 3.

## Configuração do Board

1. Acesse seu projeto e vá em **Boards > Boards**.
2. Clique no ícone de engrenagem (**Board settings**) no canto superior direito.
3. Navegue até **Columns**.
4. Crie as colunas exatamente nesta ordem, e certifique-se de marcar a opção **Split column into doing and done** para as colunas indicadas como "Sim".
5. Preencha um **WIP Limit** (limite de itens na coluna) para forçar o sistema a pintar o topo da coluna de vermelho se o time acumular gargalos.

<div style="overflow-x:auto; margin:20px 0;">
    <table style="width:100%; border-collapse:collapse; border:1px solid #e2e8f0; font-size:0.9rem;">
        <thead>
            <tr>
                <th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; border-right:1px solid #e2e8f0; text-align:left;">Nome da Coluna no Board</th>
                <th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; border-right:1px solid #e2e8f0; text-align:left;">State Vinculado (De/Para)</th>
                <th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; text-align:center;">Split Column?</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] New</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] New</code></td><td style="padding:8px; text-align:center;">Não</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] Refinamento Funcional</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] Refinamento Funcional</code></td><td style="padding:8px; text-align:center;"><strong>Sim</strong></td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] Refinamento Tecnico</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] Refinamento Tecnico</code></td><td style="padding:8px; text-align:center;"><strong>Sim</strong></td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] Aprovacao PO</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] Aprovacao PO</code></td><td style="padding:8px; text-align:center;">Não</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] Pronto para Replenishment</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] Pronto para Replenishment</code></td><td style="padding:8px; text-align:center;">Não</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Pronto para Desenvolvimento</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Pronto para Desenvolvimento</code></td><td style="padding:8px; text-align:center;">Não</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Em Desenvolvimento</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Em Desenvolvimento</code></td><td style="padding:8px; text-align:center;"><strong>Sim</strong></td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Ready to Teste</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Ready to Teste</code></td><td style="padding:8px; text-align:center;">Não</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Testando</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Testando</code></td><td style="padding:8px; text-align:center;"><strong>Sim</strong></td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Ready to Homologacao</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Ready to Homologacao</code></td><td style="padding:8px; text-align:center;">Não</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Em validacao PO</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Em validacao PO</code></td><td style="padding:8px; text-align:center;">Não</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Homologado</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Homologado</code></td><td style="padding:8px; text-align:center;">Não</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Liberado para Instalar</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Liberado para Instalar</code></td><td style="padding:8px; text-align:center;">Não</td></tr>
            <tr><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Done</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Done</code></td><td style="padding:8px; text-align:center;">Não</td></tr>
        </tbody>
    </table>
</div>

> [!TIP]
> **Board Visual:** Abaixo você vê o resultado esperado de como ficará o seu board.

  <!-- BOARD VISUAL (ELITE TEAM EXEMPLO) -->
  <div style="overflow-x:auto;padding-bottom:12px;margin-top:20px;">
    <div style="display:flex;gap:0;min-width:max-content;">

      <!-- ZONA UPSTREAM -->
      <div style="flex:1;min-width:0;">
        <div style="background:#eff6ff;border:2px solid #3b82f6;border-radius:10px 10px 0 0;padding:6px 10px;font-size:11px;font-weight:700;color:#1d4ed8;text-align:center;letter-spacing:.05em;">UPSTREAM — Descoberta & Refinamento</div>
        <div style="display:flex;gap:4px;padding:8px;background:#eff6ff;border:2px solid #3b82f6;border-top:none;border-radius:0 0 10px 10px;">

          <div style="flex:1;min-width:90px;border-radius:8px;border:2px solid #93c5fd;background:#dbeafe;padding:8px 6px;">
            <div style="font-size:10px;font-weight:700;color:#1e40af;margin-bottom:4px;">NEW</div>
            <div style="font-size:11px;color:#374151;">Buffer</div>
          </div>

          <div style="display:flex;align-items:center;color:#94a3b8;font-size:16px;padding:0 2px;">›</div>

          <div style="flex:1;min-width:90px;border-radius:8px;border:2px solid #93c5fd;background:#dbeafe;padding:8px 6px;">
            <div style="font-size:10px;font-weight:700;color:#1e40af;margin-bottom:4px;">REF. FUNCIONAL</div>
            <div style="display:flex;gap:4px;">
              <span style="font-size:10px;background:#fef08a;border-radius:4px;padding:2px 5px;color:#713f12;">Doing</span>
              <span style="font-size:10px;background:#bbf7d0;border-radius:4px;padding:2px 5px;color:#14532d;">Done</span>
            </div>
          </div>

          <div style="display:flex;align-items:center;color:#94a3b8;font-size:16px;padding:0 2px;">›</div>

          <div style="flex:1;min-width:90px;border-radius:8px;border:2px solid #93c5fd;background:#dbeafe;padding:8px 6px;">
            <div style="font-size:10px;font-weight:700;color:#1e40af;margin-bottom:4px;">REF. TÉCNICO</div>
            <div style="display:flex;gap:4px;">
              <span style="font-size:10px;background:#fef08a;border-radius:4px;padding:2px 5px;color:#713f12;">Doing</span>
              <span style="font-size:10px;background:#bbf7d0;border-radius:4px;padding:2px 5px;color:#14532d;">Done</span>
            </div>
          </div>

          <div style="display:flex;align-items:center;color:#94a3b8;font-size:16px;padding:0 2px;">›</div>

          <div style="flex:1;min-width:90px;border-radius:8px;border:2px solid #93c5fd;background:#dbeafe;padding:8px 6px;">
            <div style="font-size:10px;font-weight:700;color:#1e40af;margin-bottom:4px;">APROVAÇÃO PO</div>
          </div>
          
        </div>
      </div>

      <!-- COMMITMENT POINT -->
      <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 12px;gap:8px;">
        <div style="flex:1;width:4px;background:#ef4444;border-radius:2px;box-shadow:0 0 8px rgba(239,68,68,0.5);"></div>
        <div style="font-size:11px;font-weight:900;color:#dc2626;text-align:center;writing-mode:vertical-lr;transform:rotate(180deg);letter-spacing:.1em;">COMMITMENT POINT</div>
        <div style="flex:1;width:4px;background:#ef4444;border-radius:2px;box-shadow:0 0 8px rgba(239,68,68,0.5);"></div>
      </div>

      <!-- ZONA DOWNSTREAM DEV -->
      <div style="flex:1.6;min-width:0;">
        <div style="background:#fffbeb;border:2px solid #f59e0b;border-radius:10px 10px 0 0;padding:6px 10px;font-size:11px;font-weight:700;color:#b45309;text-align:center;letter-spacing:.05em;">DOWNSTREAM — Desenvolvimento & QA</div>
        <div style="display:flex;gap:4px;padding:8px;background:#fffbeb;border:2px solid #f59e0b;border-top:none;border-radius:0 0 10px 10px;">

          <div style="flex:1;min-width:80px;border-radius:8px;border:2px solid #d1d5db;background:#f9fafb;padding:8px 6px;">
            <div style="font-size:10px;font-weight:700;color:#374151;margin-bottom:4px;">PRONTO DESENV.</div>
          </div>

          <div style="display:flex;align-items:center;color:#94a3b8;font-size:16px;padding:0 2px;">›</div>

          <div style="flex:1;min-width:80px;border-radius:8px;border:2px solid #fcd34d;background:#fef3c7;padding:8px 6px;">
            <div style="font-size:10px;font-weight:700;color:#92400e;margin-bottom:4px;">EM DESENVOLV.</div>
            <div style="display:flex;gap:4px;">
              <span style="font-size:10px;background:#fef08a;border-radius:4px;padding:2px 5px;color:#713f12;">Doing</span>
              <span style="font-size:10px;background:#bbf7d0;border-radius:4px;padding:2px 5px;color:#14532d;">Done</span>
            </div>
          </div>

          <div style="display:flex;align-items:center;color:#94a3b8;font-size:16px;padding:0 2px;">›</div>

          <div style="flex:1;min-width:80px;border-radius:8px;border:2px solid #d1d5db;background:#f9fafb;padding:8px 6px;">
            <div style="font-size:10px;font-weight:700;color:#374151;margin-bottom:4px;">READY TO TESTE</div>
          </div>

          <div style="display:flex;align-items:center;color:#94a3b8;font-size:16px;padding:0 2px;">›</div>

          <div style="flex:1;min-width:80px;border-radius:8px;border:2px solid #fcd34d;background:#fef3c7;padding:8px 6px;">
            <div style="font-size:10px;font-weight:700;color:#92400e;margin-bottom:4px;">TESTANDO</div>
            <div style="display:flex;gap:4px;">
              <span style="font-size:10px;background:#fef08a;border-radius:4px;padding:2px 5px;color:#713f12;">Doing</span>
              <span style="font-size:10px;background:#bbf7d0;border-radius:4px;padding:2px 5px;color:#14532d;">Done</span>
            </div>
          </div>

        </div>
      </div>

      <!-- ZONA DOWNSTREAM HOMOLOG -->
      <div style="flex:1.1;min-width:0;">
        <div style="background:#f0fdf4;border:2px solid #22c55e;border-radius:10px 10px 0 0;padding:6px 10px;font-size:11px;font-weight:700;color:#15803d;text-align:center;letter-spacing:.05em;">DOWNSTREAM — Validação & Entrega</div>
        <div style="display:flex;gap:4px;padding:8px;background:#f0fdf4;border:2px solid #22c55e;border-top:none;border-radius:0 0 10px 10px;">

          <div style="flex:1;min-width:80px;border-radius:8px;border:2px solid #fcd34d;background:#fef3c7;padding:8px 6px;">
            <div style="font-size:10px;font-weight:700;color:#92400e;margin-bottom:4px;">VALIDAÇÃO PO</div>
          </div>

          <div style="display:flex;align-items:center;color:#94a3b8;font-size:16px;padding:0 2px;">›</div>

          <div style="flex:1;min-width:80px;border-radius:8px;border:2px solid #86efac;background:#dcfce7;padding:8px 6px;">
            <div style="font-size:10px;font-weight:700;color:#14532d;margin-bottom:4px;">✅ HOMOLOGADO</div>
          </div>

          <div style="display:flex;align-items:center;color:#94a3b8;font-size:16px;padding:0 2px;">›</div>

          <div style="flex:0.7;min-width:70px;border-radius:8px;border:2px solid #86efac;background:#d1fae5;padding:8px 6px;">
            <div style="font-size:10px;font-weight:700;color:#064e3b;margin-bottom:4px;">✅ DONE</div>
          </div>

        </div>
      </div>
    </div>
  </div>


<hr>
<div style="text-align: right; margin-top: 20px;">
    <strong><a href="#" onclick="document.querySelectorAll('.kb-nav-btn')[5].click(); return false;" style="color: #3b82f6; text-decoration: none;">Avançar para o Passo 6: Classes de Serviço (Swimlanes) ➔</a></strong>
</div>
