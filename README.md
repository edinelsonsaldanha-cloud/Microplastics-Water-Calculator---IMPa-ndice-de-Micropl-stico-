IMPa Software

Microplastic Index Based on Length, Count, and Area

1. Introduction

Microplastic contamination in aquatic environments represents one of the major contemporary environmental challenges. Traditional quantification methods are predominantly based on particle counting (items/L), which limits the physical and environmental interpretation of the real impact of these particles.

The IMPa Software was developed to overcome these limitations by incorporating metrics based on:

Total microplastic length (µm/L)

Projected microplastic area (µm²/L)

Traditional particle count (items/L)

These metrics allow for a more robust assessment of microplastic load, considering not only the number of particles but also their physical dimensions.

2. Objectives

The main objective of the IMPa Software is to provide an integrated tool for:

Accurate measurement of microplastics from microscopic images;

Standardization of environmental microplastic indicator calculations;

Comparison between traditional metrics and dimension-based metrics;

Automatic generation of quantitative results and statistical graphs;

Support for multivariate analyses (PCA).

3. Project Structure
IMPa_Software/
│
├── main.py
├── requirements.txt
├── README.md
│
├── core/
│   ├── calculo_impa.py
│   ├── calculo_impa_area.py
│   ├── gerar_base_pca.py
│   ├── pca_analysis.py
│   ├── pca_interpretacao.py
│   └── graficos/
│       ├── grafico_impa_por_ponto.py
│       ├── grafico_impa_por_tipo.py
│       ├── grafico_matriz_impa.py
│       ├── grafico_boxplot_comprimentos.py
│       ├── grafico_boxplot_area.py
│       ├── grafico_impa_area_por_ponto.py
│       ├── grafico_impa_area_por_tipo.py
│       └── grafico_percentual_impa_area.py
│
├── gui/
│   ├── tela_inicial.py
│   ├── tela_medicao.py
│   ├── tela_resultados.py
│   ├── tela_calibracao.py
│   ├── tela_criacao_projeto.py
│   ├── tela_Pontos_Amostrais.py
│   └── main_window.py
│
├── resources/
│   └── logos/
│
└── dados/

4. Methodology
4.1 Microplastic Measurement

Measurements are performed using calibrated microscopic images. The user can:

Mark consecutive points to measure length;

Close a polygon to calculate projected area;

Classify each microplastic by type (fiber, fragment, film, pellet, other).

Area calculation is only allowed when the polygon is explicitly closed, ensuring geometric rigor.

4.2 Traditional IMPa Calculation (Length-Based)

The length-based index is defined as:

IMPa=(∑L_i)/V


where:

𝐿
is the individual microplastic length (µm);

𝑉
V is the sample volume (L).

Results are presented:

By sampling point;

By microplastic type;

Globally.

4.3 Area-Based IMPa Calculation

The area-based index is defined as:

IMPa_(A ˊrea)=(∑A_i)/V

where:

 is the projected microplastic area (µm²);

𝑉
V is the sample volume (L).

This metric more accurately represents the potential environmental interaction surface.

4.4 Traditional Microplastic Count

Traditional microplastic concentration is expressed as:

MP=N/V

where:

𝑁
N is the number of microplastics;

𝑉
V is the sample volume (L).

5. Generated Results
Numerical Indicators

IMPa per sampling point (µm/L)

IMPa per microplastic type (µm/L)

Global IMPa (µm/L)

MP per sampling point (items/L)

MP per microplastic type (items/L)

Global MP (items/L)

Area-based IMPa per sampling point (µm²/L)

Area-based IMPa per microplastic type (µm²/L)

Global area-based IMPa (µm²/L)

Graphical Outputs

Length distribution

Length boxplots

Area boxplots

IMPa per sampling point

IMPa per microplastic type

Percentage IMPa by type

Matrix plots (Sampling Point × Type)

Equivalent graphs for area-based IMPa

Principal Component Analysis (PCA)

6. Graphical User Interface

The graphical interface was developed using PySide6 (Qt) and includes:

Interactive measurement interface;

Editing, removal, and deletion of microplastics;

Integrated results interface;

Automatic export of results;

Compatibility with executable format (.exe).

7. Requirements

Python ≥ 3.10

PySide6

NumPy

OpenCV

Pandas

Matplotlib

Installation
pip install -r requirements.txt

8. Execution
python main.py


Or via executable:

IMPa.exe

9. Applications

The IMPa Software can be used in:

Academic research;

Environmental monitoring;

Undergraduate and graduate projects;

Technical reports;

Institutional environmental quality programs.

10. Citation

If you use this software, please cite it as:

Edinelson Saldanha.
IMPa Software: Microplastic Index Based on Length and Area.
Version 1.0. 2026. DOI: XXXXX.

11. License

This software is distributed under the MIT License, allowing use, modification, and distribution, provided that the original authorship is properly cited.


Em Português


IMPa Software
Índice de Microplásticos baseado em Comprimento, Contagem e Área
1. Introdução
A contaminação por microplásticos em ambientes aquáticos representa um dos principais desafios ambientais contemporâneos. Métodos tradicionais de quantificação baseiam-se majoritariamente na contagem de partículas (itens/L), o que limita a interpretação física e ambiental do impacto real dessas partículas.
O IMPa Software foi desenvolvido para superar essas limitações, incorporando métricas baseadas em:
	Comprimento total de microplásticos (µm/L)
	Área projetada de microplásticos (µm²/L)
	Contagem tradicional (itens/L)
Essas métricas permitem uma análise mais robusta da carga microplástico, considerando não apenas o número de partículas, mas também sua dimensão física.

2. Objetivos
O objetivo principal do IMPa Software é fornecer uma ferramenta integrada para:
	Medição precisa de microplásticos a partir de imagens microscópicas;
	Padronização do cálculo de indicadores ambientais de microplásticos;
	Comparação entre métricas tradicionais e métricas baseadas em dimensão física;
	Geração automática de resultados quantitativos e gráficos estatísticos;
	Suporte a análises multivariadas (PCA).





3. Estrutura do Projeto
IMPa_Software/
│
├── main.py
├── requirements.txt
├── README.md
│
├── core/
│   ├── calculo_impa.py
│   ├── calculo_impa_area.py
│   ├── gerar_base_pca.py
│   ├── pca_analysis.py
│   ├── pca_interpretacao.py
│   └── graficos/
│       ├── grafico_impa_por_ponto.py
│       ├── grafico_impa_por_tipo.py
│       ├── grafico_matriz_impa.py
│       ├── grafico_boxplot_comprimentos.py
│       ├── grafico_boxplot_area.py
│       ├── grafico_impa_area_por_ponto.py
│       ├── grafico_impa_area_por_tipo.py
│       └── grafico_percentual_impa_area.py
│
├── gui/
│   ├── tela_inicial.py
│   ├── tela_medicao.py
│   ├── tela_resultados.py
│   ├── tela_calibracao.py
│   ├── tela_criacao_projeto.py
│   ├── tela_Pontos_Amostrais.py
│   └── main_window.py
│
├── resources/
│   └── logos/
│
└── dados/




4. Metodologia
4.1 Medição de Microplásticos
As medições são realizadas a partir de imagens microscópicas calibradas. O usuário pode:
	Marcar pontos consecutivos para medir comprimento;
	Fechar um polígono para cálculo de área projetada;
	Classificar cada microplástico por tipo (fibra, fragmento, filme, pellet, outro).
O cálculo de área só é permitido quando o polígono está explicitamente fechado, garantindo rigor geométrico.

4.2 Cálculo do IMPa Tradicional (Comprimento)
O índice baseado em comprimento é definido como:
IMPa=(∑L_i)/V

onde:
	L_ié o comprimento individual do microplástico (µm);
	Vé o volume da amostra (L).
Resultados são apresentados:
	Por ponto amostral;
	Por tipo de microplástico;
	Globalmente.

4.3 Cálculo do IMPa–Área
O índice baseado em área é definido como:
IMPa_(A ˊrea)=(∑A_i)/V

onde:
	A_ié a área projetada do microplástico (µm²);
	Vé o volume da amostra (L).
Essa métrica representa de forma mais fiel a superfície potencial de interação ambiental.

4.4 MP Tradicional (Contagem)
A contagem tradicional é expressa como:
MP=N/V

onde:
	Né o número de microplásticos;
	Vé o volume da amostra (L).

5. Resultados Gerados
O software gera automaticamente:
Indicadores Numéricos
	IMPa por ponto (µm/L)
	IMPa por tipo (µm/L)
	IMPa global (µm/L)
	MP por ponto (itens/L)
	MP por tipo (itens/L)
	MP global (itens/L)
	IMPa–Área por ponto (µm²/L)
	IMPa–Área por tipo (µm²/L)
	IMPa–Área global (µm²/L)
Gráficos
	Distribuição de comprimentos
	Boxplot de comprimentos
	Boxplot de áreas
	IMPa por ponto
	IMPa por tipo
	IMPa percentual por tipo
	Matrizes (Ponto × Tipo)
	Gráficos equivalentes para IMPa–Área
	Análise de Componentes Principais (PCA)

6. Interface Gráfica
A interface gráfica foi desenvolvida com PySide6 (Qt) e inclui:
	Tela de medição interativa;
	Edição, remoção e exclusão de microplásticos;
	Tela de resultados integrada;
	Exportação automática de resultados;
	Compatibilidade com executável (.exe).

7. Requisitos
	Python ≥ 3.10
	PySide6
	NumPy
	OpenCV
	Pandas
	Matplotlib

Instalação:
pip install -r requirements.txt

8. Execução
python main.py
Ou via executável:
IMPa.exe

9. Aplicações
O IMPa Software pode ser utilizado em:
	Pesquisas acadêmicas;
	Monitoramento ambiental;
	Projetos de graduação e pós-graduação;
	Relatórios técnicos;
	Programas institucionais de qualidade ambiental.

10. Citação
Ao utilizar este software, cite como:
Edinelson Saldanha. IMPa Software: Índice de Microplásticos baseado em Comprimento e Área. Versão 1.0. Ano 2026. DOI: XXXXX.

11. Licença
Este software é distribuído sob a licença MIT, permitindo uso, modificação e distribuição, desde que citada a autoria original.

