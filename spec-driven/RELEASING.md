# Release — checklist

Passos para publicar `@igoruehara/spec-driven` no npm. O GitHub já está publicado;
isto cobre o npm e a tag de versão.

## 0. Pré-requisitos (uma vez)
- [ ] Conta npm cujo **username é `igoruehara`** (o escopo `@igoruehara` precisa ser seu).
      Se for outro nome, ajuste `name` no `package.json` para `@<seu-user>/spec-driven`.

## 1. Login e verificação
```bash
npm login            # usuário, senha e OTP (2FA)
npm whoami           # deve retornar: igoruehara
```

## 2. Conferir o que vai pro pacote
```bash
npm run pack:check   # = npm pack --dry-run  → confere os ~42 arquivos (inclui template/.claude)
npm run test:scaffold # scaffolda numa pasta de teste e valida a CLI
```

## 3. Versão (semver)
```bash
npm version patch    # 0.1.0 → 0.1.1   (use minor/major conforme a mudança)
```
> `npm version` cria o commit e a tag `vX.Y.Z` automaticamente.

## 4. Publicar
```bash
npm publish                 # access:public já está no package.json
# se o 2FA pedir código na hora:
npm publish --otp=123456
```
> O `prepublishOnly` roda um smoke test da CLI antes de publicar — se a CLI quebrar, o publish aborta.

## 5. Empurrar tag + release no GitHub
```bash
git push --follow-tags
gh release create v$(node -p "require('./package.json').version") --generate-notes
```

## 6. Confirmar
```bash
npm view @igoruehara/spec-driven version
npx @igoruehara/spec-driven --help   # ou rode num diretório de teste
```

---

## Sem npm (alternativa)
O pacote roda direto do GitHub a qualquer momento:
```bash
npx github:igoruehara/spec-driven
```
