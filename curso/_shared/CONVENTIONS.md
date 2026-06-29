# CONVENTIONS — oscoach (LEIA ANTES DE CONSTRUIR QUALQUER PÁGINA)

Doc curto para os builders das trilhas/módulos. A **foundation** (landing +
`curso/trilha1/index.html` + `curso/trilha1/modulo-1-1.html`) é o padrão-ouro: copie a
estrutura dela. Aqui ficam só as convenções travadas que TODA página precisa respeitar.

## 0. courseId (travado)
- `courseId = oscoach`. Em TODA página: `<meta name="inema-course" content="oscoach">`.
- O manifesto e o storage usam esse id (`inema.oscoach.*`). Não invente outro.

## 1. Ordem do `<head>` (obrigatória — Erros #18/#28)
1. `<meta charset>` + `<meta viewport>` + `<meta name="inema-course" content="oscoach">`
2. **Anti-FOUC** (snippet `_shared/head-antifouc.html`) — PRIMEIRO script, antes do Tailwind.
3. **Manifesto** — `<script type="application/json" data-inema-manifest>` com o conteúdo
   de `_shared/manifest.json` **verbatim** (idêntico em todas as páginas).
4. Tailwind CDN + `tailwind.config` (primary `#FACC15`, paleta `dark`).
5. Google Fonts (Inter).
6. `<style>` com o CSS base v1 + **Light mode** (Sec. 1.5: 4 partes) + Parte 5 (bordas
   dark suavizadas) + a regra de SVG no claro.
7. `<link rel="stylesheet" href="REL/assets/learn.css">` — DEPOIS do CSS base.

## 2. Fim do `<body>` (obrigatório)
- As 3 funções-núcleo v1 inline: `toggleTopic`, theme toggle (sol/lua), `openModal/closeModal`.
- Depois: `_shared/init.html` → `<script src="REL/assets/learn.js">` + `INEMA.init()` por ÚLTIMO.
- Em página de MÓDULO pode usar `INEMA.init({ autoResume: true })`.

## 3. Caminhos relativos por profundidade (REL)
| Página | REL (assets) | learn.css / learn.js |
|---|---|---|
| Landing `index.html` (raiz) | `.` | `assets/learn.css` · `assets/learn.js` |
| `curso/trilhaN/index.html` e `curso/trilhaN/modulo-N-Y.html` | `../..` | `../../assets/learn.css` · `../../assets/learn.js` |

Nav (ver `_shared/nav.html`): logo → `../../index.html` (em curso/trilhaN/) ou `index.html`
(landing). Trilha ativa → `index.html`; outras → `../trilhaM/index.html`. Na landing, todas
as trilhas → `curso/trilhaM/index.html` e nenhuma fica ativa.

## 4. `data-inema-*` — contrato de ancoragem (Erro #19). TOKENS NUMÉRICOS.
> **DECISÃO TRAVADA (lendo o código real de `learn.js` `keyParts`):** o **track** é
> derivado do id do tópico — `modulo-1-1#topico-3` → módulo `1-1` → track `1` (primeiro
> segmento). Por isso `data-inema-track`, o `n` do manifesto e o escopo `trilha:N` usam o
> **número** `1`..`5` — **NÃO** `trilha1`. A pasta continua `trilhaN`; o atributo é só o número.

Markup por página de MÓDULO (`curso/trilhaN/modulo-N-Y.html`):
```html
<!-- elemento exterior do conteúdo do módulo -->
<main id="conteudo" data-inema-module="N-Y" data-inema-track="N"> … </main>

<!-- cada um dos K tópicos é uma <section> -->
<section id="topico-3" data-inema-topic="modulo-N-Y#topico-3"
         class="mb-16" style="scroll-margin-top:5rem"> … </section>

<!-- prosa anotável: blockId determinístico mN-Y-tT-pP -->
<p data-inema-block="m1-1-t3-p2"> … </p>
```
- `data-inema-topic` = `modulo-N-Y#topico-T` (T = ordem estável 1..K). É o id de
  progresso/notas — **não** depende de classe visual.
- `data-inema-module` = `N-Y` (ex.: `1-1`). `data-inema-track` = `N` (ex.: `1`).
- O nº de `[data-inema-topic]` no DOM do módulo **tem que bater** com o `topics` daquele
  módulo no manifesto (LOCKED — ver tabela §6). Divergiu → % do curso quebra (#28).

## 5. Controles da camada de aprendizagem
- **Marcar lido** (1 por `<section>` de tópico): `<button data-inema-read-toggle
  aria-pressed="false">` com os 4 spans canônicos `inema-ico-todo/inema-ico-done/
  inema-label-todo/inema-label-done`. Sempre `justify-start` (#1/#20). O JS pega o id do
  `[data-inema-topic]` ancestral.
- **Dúvida** (por tópico): `<button data-inema-doubt-toggle aria-pressed="false">`.
- **Medidores**: `data-inema-meter="curso" | "trilha:N" | "modulo:N-Y"`. Anel = `class="inema-ring"`
  + `<span class="inema-ring__value" data-inema-meter-pct>`. Barra = `.inema-bar` +
  `.inema-bar__fill[data-inema-meter-fill]` + slots `[data-inema-meter-pct]`/`[data-inema-meter-frac]`.
  O JS deriva % do read-map sobre o manifesto — nunca persista %.
- **TOC + scrollspy** (módulo): `<nav data-inema-toc>` com `<a href="#topico-T">` por seção.
- **Accordions** (tópicos no índice de trilha): mantêm `onclick="toggleTopic(this)"` +
  `aria-expanded` + `aria-controls` no painel `.topic-explanation` (#26).
- **Jornada / Aparência**: já vêm no nav (`_shared/nav.html`) — não duplicar a lógica.

## 6. Manifesto — módulos e contagem de tópicos (LOCKED)
Use `_shared/manifest.json` verbatim. Contagens travadas (= nº de `[data-inema-topic]` reais):

| Trilha (cor) | Módulos · tópicos |
|---|---|
| trilha1 Fundamentos (Emerald) | 1-1 ·7 · 1-2 ·7 · 1-3 ·8 |
| trilha2 Técnica I · Base (Blue) | 2-1 ·8 · 2-2 ·8 · 2-3 ·8 |
| trilha3 Técnica II · Capacidade (Purple) | 3-1 ·8 · 3-2 ·8 · 3-3 ·8 |
| trilha4 Passo a passo (Amber) | 4-1 ·7 · 4-2 ·7 · 4-3 ·7 · 4-4 ·7 · 4-5 ·7 · 4-6 ·8 |
| trilha5 Avançado (Teal) | 5-1 ·7 · 5-2 ·7 · 5-3 ·7 · 5-4 ·7 · 5-5 ·7 · 5-6 ·7 |

- `href` no manifesto é **relativo à RAIZ do curso** (ex.: `curso/trilha2/modulo-2-1.html`)
  e o manifesto é IDÊNTICO em toda página. (Convenção do LEARN-LAYER §1.7. A agregação de
  progresso casa por `id`, não por `href`, então hrefs root-relative não afetam o %.)

## 7. Cores por trilha (chrome Tailwind)
emerald (T1) · blue (T2) · purple (T3) · amber (T4) · teal (T5). Diagramas SVG: cor da
trilha = primária, ciano `#38bdf8` = secundária. Light mode de cada trilha: ver Sec. 1.5
do MASTER (amber usa -800 no texto, nunca âmbar como texto em fundo claro — #23).

## 8. Antes de entregar
Rode o `CHECKLIST_REVISAO.md` (trilha OU módulo) + os erros #18–#31. Não regrida #1–#17.
