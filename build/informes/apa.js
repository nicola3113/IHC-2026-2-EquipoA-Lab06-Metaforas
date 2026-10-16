// Utilidades comunes para los informes del Laboratorio 6 en formato APA 7 (trabajo estudiantil).
// Times New Roman 12, interlineado doble, márgenes de 2,54 cm, números de página arriba a la derecha,
// títulos APA en negro, tablas con solo líneas horizontales, figuras numeradas con nota y referencias
// con sangría francesa. Sin colores: los hipervínculos se muestran en negro.
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, BorderStyle, ImageRun, PageBreak, LevelFormat, Header, PageNumber, TableOfContents,
  ExternalHyperlink,
} = require('docx');

const FONT = 'Times New Roman';
const RAIZ = path.resolve(__dirname, '..', '..');
const ANCHO_UTIL = 9026; // A4 con márgenes de 2,54 cm, en DXA

// Texto con marcas ligeras: **negrita**, *cursiva*, `código`
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const t = m[0];
    if (t.startsWith('**')) out.push(new TextRun({ text: t.slice(2, -2), bold: true, ...base }));
    else if (t.startsWith('`')) out.push(new TextRun({ text: t.slice(1, -1), font: 'Courier New', ...base, size: (base.size || 24) - 2 }));
    else out.push(new TextRun({ text: t.slice(1, -1), italics: true, ...base }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}
const p = (text) => new Paragraph({ indent: { firstLine: 720 }, children: runs(text) });
const pSinSangria = (text) => new Paragraph({ children: runs(text) });
const centro = (children, opts = {}) => new Paragraph({ alignment: AlignmentType.CENTER, ...opts, children });
const h1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: runs(t) });
const h2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: runs(t) });
const h3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: runs(t) });
const vineta = (t) => new Paragraph({ numbering: { reference: 'vinetas', level: 0 }, children: runs(t) });
const numerado = (t, ref = 'numeros') => new Paragraph({ numbering: { reference: ref, level: 0 }, children: runs(t) });
const enlace = (url, texto) => new ExternalHyperlink({ link: url, children: [new TextRun({ text: texto || url, style: 'Hyperlink' })] });
const salto = () => new Paragraph({ children: [new PageBreak()] });
const parrafoEnlace = (etiqueta, url) => new Paragraph({ indent: { left: 720 }, children: [new TextRun({ text: etiqueta, bold: true }), enlace(url)] });

// ------------------------------------------------------------------ tablas APA
const NINGUNO = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const LINEA = { style: BorderStyle.SINGLE, size: 8, color: '000000' };
let nTabla = 0, nFigura = 0;
function reiniciarContadores() { nTabla = 0; nFigura = 0; }
function tabla(titulo, encabezados, filas, anchos, nota) {
  nTabla++;
  const total = anchos.reduce((a, b) => a + b, 0);
  const escala = total > ANCHO_UTIL ? ANCHO_UTIL / total : 1;
  const w = anchos.map(a => Math.round(a * escala));
  const celda = (txt, i, o) => new TableCell({
    width: { size: w[i], type: WidthType.DXA },
    borders: { top: o.arriba ? LINEA : NINGUNO, bottom: o.abajo ? LINEA : NINGUNO, left: NINGUNO, right: NINGUNO },
    margins: { top: 40, bottom: 40, left: 90, right: 90 },
    children: String(txt).split('\n').map(linea => new Paragraph({
      spacing: { line: 240, after: 0 }, children: runs(linea, { size: 20, bold: o.cab || undefined }),
    })),
  });
  const ultima = filas.length - 1;
  return [
    new Paragraph({ keepNext: true, spacing: { before: 240 }, children: [new TextRun({ text: `Tabla ${nTabla}`, bold: true })] }),
    new Paragraph({ keepNext: true, children: [new TextRun({ text: titulo, italics: true })] }),
    new Table({
      width: { size: w.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: w,
      borders: { top: NINGUNO, bottom: NINGUNO, left: NINGUNO, right: NINGUNO, insideHorizontal: NINGUNO, insideVertical: NINGUNO },
      rows: [
        new TableRow({ tableHeader: true, children: encabezados.map((h, i) => celda(h, i, { cab: true, arriba: true, abajo: true })) }),
        ...filas.map((fila, k) => new TableRow({ cantSplit: true, children: fila.map((c, i) => celda(c, i, { abajo: k === ultima })) })),
      ],
    }),
    nota ? new Paragraph({ spacing: { line: 240, before: 120, after: 240 }, children: [new TextRun({ text: 'Nota. ', italics: true, size: 20 }), ...runs(nota, { size: 20 })] })
         : new Paragraph({ spacing: { line: 240, after: 120 }, children: [] }),
  ];
}

// ------------------------------------------------------------------ figuras
function dimensiones(buf) {
  if (buf.readUInt32BE(0) === 0x89504e47) return [buf.readUInt32BE(16), buf.readUInt32BE(20)]; // PNG
  let i = 2;                                                                                       // JPEG
  while (i < buf.length) {
    if (buf[i] !== 0xff) { i++; continue; }
    const marca = buf[i + 1], largo = buf.readUInt16BE(i + 2);
    if (marca >= 0xc0 && marca <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(marca)) return [buf.readUInt16BE(i + 7), buf.readUInt16BE(i + 5)];
    i += 2 + largo;
  }
  throw new Error('Formato de imagen no reconocido');
}
function figura(rutaRelativa, titulo, nota, anchoPx = 600, altoMax = 820) {
  nFigura++;
  const archivo = path.join(RAIZ, rutaRelativa);
  const buf = fs.readFileSync(archivo);
  const [w, h] = dimensiones(buf);
  let ancho = anchoPx, alto = Math.round(anchoPx * h / w);
  if (alto > altoMax) { alto = altoMax; ancho = Math.round(altoMax * w / h); }
  return [
    new Paragraph({ keepNext: true, spacing: { before: 240 }, children: [new TextRun({ text: `Figura ${nFigura}`, bold: true })] }),
    new Paragraph({ keepNext: true, children: [new TextRun({ text: titulo, italics: true })] }),
    new Paragraph({ keepNext: true, spacing: { line: 240 }, alignment: AlignmentType.CENTER, children: [
      new ImageRun({ type: /\.png$/i.test(archivo) ? 'png' : 'jpg', data: buf, transformation: { width: ancho, height: alto },
        altText: { title: titulo, description: titulo, name: path.basename(archivo) } }),
    ] }),
    new Paragraph({ spacing: { line: 240, before: 120, after: 240 }, children: [new TextRun({ text: 'Nota. ', italics: true, size: 20 }), ...runs(nota, { size: 20 })] }),
  ];
}
const siguienteFigura = () => nFigura + 1;
const siguienteTabla = () => nTabla + 1;

// ------------------------------------------------------------------ carátula y referencias
const INTEGRANTES = [
  ['Arboleda Sánchez, Ericka Sofía', '24200047'], ['Cabrejos Palomino, Christian Daniel', '23200242'],
  ['Ccoicca Fernández, Adrián', '24200154'], ['Cerna Sifuentes, Augusto Nicolás', '24200053'],
  ['Grijalva De La Cruz, Rony Smith', '24200058'], ['Martines Cancho, Josué', '24200060'],
  ['Postigo Vega, Diana Carolina', '24200167'], ['Siesquen Torres, Katherine Lizbeth', '24200066'],
  ['Tecsi Alanoca, Jean Carlo', '24200068'], ['Tonconi Isidro, María Sunori', '24200176'],
  ['Villegas Niño, Marco Antonio', '21200266'],
];
function caratula(titulo, subtitulo, fecha) {
  const escudo = fs.readFileSync(path.join(__dirname, 'escudo_apa.png'));
  const l = (t, o = {}) => centro([new TextRun({ text: t, ...o })], { spacing: { line: 276, after: 0 } });
  return [
    l('UNIVERSIDAD NACIONAL MAYOR DE SAN MARCOS', { bold: true }),
    l('Universidad del Perú, Decana de América', { italics: true }),
    l('Facultad de Ingeniería de Sistemas e Informática'),
    l('Escuela Profesional de Ingeniería de Software'),
    centro([new ImageRun({ type: 'png', data: escudo, transformation: { width: 120, height: 120 },
      altText: { title: 'Escudo UNMSM', description: 'Escudo de la Universidad Nacional Mayor de San Marcos', name: 'escudo' } })], { spacing: { before: 200, after: 200, line: 240 } }),
    centro(runs(`**${titulo}**`), { spacing: { line: 360, after: 120 } }),
    l(subtitulo),
    new Paragraph({ spacing: { line: 240 }, children: [] }),
    l('Equipo A', { bold: true }),
    ...INTEGRANTES.map(([n, c]) => l(`${n} — ${c}`)),
    new Paragraph({ spacing: { line: 240 }, children: [] }),
    l('Curso: Interacción Hombre-Computador (202W0606)'),
    l('Docente: Mg. Ing. Ernesto D. Cancho-Rodríguez, MBA (GWU)'),
    l('Semestre académico 2026-2'),
    l(`Lima, ${fecha}`),
    salto(),
  ];
}
const indice = () => [
  centro([new TextRun({ text: 'Índice', bold: true })]),
  new TableOfContents('Índice', { hyperlink: true, headingStyleRange: '1-3' }),
  salto(),
];
// referencias: [texto con marcas, url|null]
const referencias = (lista) => lista.map(([texto, url]) => new Paragraph({ indent: { left: 720, hanging: 720 }, children: [
  ...runs(texto), ...(url ? [new TextRun(' '), enlace(url)] : []),
] }));

function documento(titulo, hijos) {
  return new Document({
    creator: 'Equipo A — IHC 2026-2 (UNMSM)',
    title: titulo,
    features: { updateFields: true },
    styles: {
      default: { document: { run: { font: FONT, size: 24, color: '000000' }, paragraph: { spacing: { line: 480 } } } },
      characterStyles: [{ id: 'Hyperlink', name: 'Hyperlink', basedOn: 'DefaultParagraphFont', run: { color: '000000', underline: {} } }],
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { font: FONT, size: 24, bold: true, color: '000000' },
          paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 240, after: 0, line: 480 }, keepNext: true, outlineLevel: 0 } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { font: FONT, size: 24, bold: true, color: '000000' },
          paragraph: { spacing: { before: 120, after: 0, line: 480 }, keepNext: true, outlineLevel: 1 } },
        { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { font: FONT, size: 24, bold: true, italics: true, color: '000000' },
          paragraph: { spacing: { before: 0, after: 0, line: 480 }, keepNext: true, outlineLevel: 2 } },
      ],
    },
    numbering: { config: [
      { reference: 'vinetas', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      ...['numeros', 'numeros2', 'numeros3', 'numeros4', 'numeros5', 'numeros6'].map(ref => ({ reference: ref, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] })),
    ] },
    sections: [{
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440, header: 720 } } },
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { line: 240 }, children: [new TextRun({ children: [PageNumber.CURRENT] })] })] }) },
      children: hijos,
    }],
  });
}
async function guardar(doc, ruta) {
  fs.mkdirSync(path.dirname(ruta), { recursive: true });
  fs.writeFileSync(ruta, await Packer.toBuffer(doc));
  console.log('Generado:', ruta);
}

// Referencias verificadas (Crossref y acceso a la URL el 16/10/2026); se citan en ambos informes según corresponda
const REF = {
  blackwell: ['Blackwell, A. F. (2006). The reification of metaphor as a design tool. *ACM Transactions on Computer-Human Interaction, 13*(4), 490–530.', 'https://doi.org/10.1145/1188816.1188820'],
  carroll: ['Carroll, J. M. y Mack, R. L. (1985). Metaphor, computing systems, and active learning. *International Journal of Man-Machine Studies, 22*(1), 39–57.', 'https://doi.org/10.1016/S0020-7373(85)80076-6'],
  desai: ['Desai, S., Dubiel, M. y Leiva, L. A. (2024). Examining humanness as a metaphor to design voice user interfaces. En *ACM Conversational User Interfaces 2024 (CUI ’24)* (pp. 1–15). Association for Computing Machinery.', 'https://doi.org/10.1145/3640794.3665535'],
  deque: ['Deque Systems. (2024, 23 de octubre). *axe-core* (Versión 4.10.2) [Software].', 'https://github.com/dequelabs/axe-core'],
  friedman: ['Friedman, M. (1937). The use of ranks to avoid the assumption of normality implicit in the analysis of variance. *Journal of the American Statistical Association, 32*(200), 675–701.', 'https://doi.org/10.1080/01621459.1937.10503522'],
  holm: ['Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics, 6*(2), 65–70.', 'https://www.jstor.org/stable/4615733'],
  hunter: ['Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering, 9*(3), 90–95.', 'https://doi.org/10.1109/MCSE.2007.55'],
  lakoff: ['Lakoff, G. y Johnson, M. (2003). *Metaphors we live by*. University of Chicago Press. (Obra original publicada en 1980)', 'https://press.uchicago.edu/ucp/books/book/chicago/M/bo3637992.html'],
  lucide: ['Lucide Contributors. (2024, 20 de diciembre). *Lucide* (Versión 0.469.0) [Biblioteca de iconos].', 'https://lucide.dev'],
  mckinney: ['McKinney, W. (2010). Data structures for statistical computing in Python. En S. van der Walt y J. Millman (Eds.), *Proceedings of the 9th Python in Science Conference* (pp. 56–61).', 'https://doi.org/10.25080/Majora-92bf1922-00a'],
  mdn: ['MDN Web Docs. (2024, 17 de diciembre). *performance.now()*. Mozilla.', 'https://developer.mozilla.org/es/docs/Web/API/Performance/now'],
  nielsen: ['Nielsen, J. (2024, 30 de enero). *10 usability heuristics for user interface design*. Nielsen Norman Group.', 'https://www.nngroup.com/articles/ten-usability-heuristics/'],
  norman: ['Norman, D. A. (2013). *The design of everyday things* (Ed. rev. y ampliada). Basic Books.', 'https://www.hachettebookgroup.com/titles/don-norman/the-design-of-everyday-things/9780465050659/'],
  sauro: ['Sauro, J. y Dumas, J. S. (2009). Comparison of three one-question, post-task usability questionnaires. En *Proceedings of the SIGCHI Conference on Human Factors in Computing Systems* (pp. 1599–1608). Association for Computing Machinery.', 'https://doi.org/10.1145/1518701.1518946'],
  seabold: ['Seabold, S. y Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. En S. van der Walt y J. Millman (Eds.), *Proceedings of the 9th Python in Science Conference* (pp. 92–96).', 'https://doi.org/10.25080/Majora-92bf1922-011'],
  shneiderman: ['Shneiderman, B. (1983). Direct manipulation: A step beyond programming languages. *Computer, 16*(8), 57–69.', 'https://doi.org/10.1109/MC.1983.1654471'],
  virtanen: ['Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D., Burovski, E., Peterson, P., Weckesser, W., Bright, J., van der Walt, S. J., Brett, M., Wilson, J., Millman, K. J., Mayorov, N., Nelson, A. R. J., Jones, E., Kern, R., Larson, E., … van Mulbregt, P. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods, 17*(3), 261–272.', 'https://doi.org/10.1038/s41592-019-0686-2'],
  w3c: ['World Wide Web Consortium. (2024, 12 de diciembre). *Web Content Accessibility Guidelines (WCAG) 2.2* (W3C Recommendation).', 'https://www.w3.org/TR/WCAG22/'],
  wilcoxon: ['Wilcoxon, F. (1945). Individual comparisons by ranking methods. *Biometrics Bulletin, 1*(6), 80–83.', 'https://doi.org/10.2307/3001968'],
};

module.exports = { RAIZ, runs, p, pSinSangria, centro, h1, h2, h3, vineta, numerado, enlace, salto, parrafoEnlace, tabla, figura,
  caratula, indice, referencias, documento, guardar, REF, INTEGRANTES, reiniciarContadores, siguienteFigura, siguienteTabla, TextRun, Paragraph };
