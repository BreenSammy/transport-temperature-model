%###################################################################################################
%--- FTMlatex --------------------------------------------------------------------------------------
%###################################################################################################
% Description:       Auto-generated class supplying all modules and styles of the FTMlatex-project
%
% License:           Copyright (c) 2017 Technical University of Munich (https://www.tum.de/) This
%                    work may be distributed and/or modified under the conditions of the LaTeX
%                    Project Public License, either version 1.3 of this license or (at your option)
%                    any later version. The latest version of this license is in http://www.latex-
%                    project.org/lppl.txt and version 1.3 or later is part of all distributions of
%                    LaTeX version 2005/12/01 or later. This work has the LPPL maintenance status
%                    'maintained'. The current maintainer of this work is Philipp Seiwald
%                    (philipp.seiwald@tum.de).
%
% Build-Date:        05.07.2018
% Build-Time:        14:55:32
% Git Branch:        ftm/ponn/updatestudentthesis
% Git Commit Hash:   837979c (837979c17afb209420f40910b99e35ca364038eb)
%---------------------------------------------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}[1994/06/01]%
\ProvidesClass{FTMlatex}[2018/07/05 FTMlatex]%
%
% \pdfminorversion=4%
% \pdfobjcompresslevel=0%
%###################################################################################################
%--- OPTIONS ---------------------------------------------------------------------------------------
%###################################################################################################
% List of available options:
% --------------------------
% FTMcore                        (module)
% FTMfont                        (module)
% --> optHelvetica               (module-option)
% --> optArial                   (module-option)
% --> optCharter                 (module-option)
% --> optComputerModern          (module-option)
% --> optCharterMath             (module-option)
% --> optComputerModernMath      (module-option)
% FTMlang                        (module)
% --> optGerman                  (module-option)
% --> optEnglish                 (module-option)
% FTMcolor                       (module)
% --> optRGB                     (module-option)
% --> optCMYK                    (module-option)
% --> optGray                    (module-option)
% --> optMonochrome              (module-option)
% FTMtikz                        (module)
% --> optTikzExternalize         (module-option)
% FTMlogo                        (module)
% FTMmath                        (module)
% --> optLeftEquations           (module-option)
% --> optCenterEquations         (module-option)
% FTMlayout                      (module)
% --> optAfour                   (module-option)
% --> optAzero                   (module-option)
% --> optBeamerClassicFormat     (module-option)
% --> optBeamerWideFormat        (module-option)
% --> optExzellenz               (module-option)
% FTMbiblio                      (module)
% --> optBiber                   (module-option)
% --> optBibtex                  (module-option)
% --> optBibstyleNumeric         (module-option)
% --> optBibstyleAlphabetic      (module-option)
% --> optBibstyleAuthorYear      (module-option)
% FTMnames                       (module)
% FTMutils                       (module)
% --> optHideTodos               (module-option)
% --> optHideAnnotations         (module-option)
% FTMref                         (module)
% FTMbeamer                      (style)
% FTMdocument                    (style)
% FTMdocumentation               (style)
% FTMempty                       (style)
% FTMphdexpose                   (style)
% FTMphdthesis                   (style)
% FTMposter                      (style)
% FTMstudentthesis               (style)
%
% Main class options: (for enabling/disabling modules and selecting styles)
% -------------------
% Modules:
\DeclareOption{FTMcore}{\def\optFTMcore{x}}%
\DeclareOption{FTMfont}{\def\optFTMfont{x}}%
\DeclareOption{FTMlang}{\def\optFTMlang{x}}%
\DeclareOption{FTMcolor}{\def\optFTMcolor{x}}%
\DeclareOption{FTMtikz}{\def\optFTMtikz{x}}%
\DeclareOption{FTMlogo}{\def\optFTMlogo{x}}%
\DeclareOption{FTMmath}{\def\optFTMmath{x}}%
\DeclareOption{FTMlayout}{\def\optFTMlayout{x}}%
\DeclareOption{FTMbiblio}{\def\optFTMbiblio{x}}%
\DeclareOption{FTMnames}{\def\optFTMnames{x}}%
\DeclareOption{FTMutils}{\def\optFTMutils{x}}%
\DeclareOption{FTMref}{\def\optFTMref{x}}%
%
% Styles: (+ passing global options to baseclass)
\DeclareOption{FTMbeamer}{\def\optFTMbeamer{x}\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}}%
\DeclareOption{FTMdocument}{\def\optFTMdocument{x}\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}}%
\DeclareOption{FTMdocumentation}{\def\optFTMdocumentation{x}\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}}%
\DeclareOption{FTMempty}{\def\optFTMempty{x}\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}}%
\DeclareOption{FTMphdexpose}{\def\optFTMphdexpose{x}\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}}%
\DeclareOption{FTMphdthesis}{\def\optFTMphdthesis{x}\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}}%
\DeclareOption{FTMposter}{\def\optFTMposter{x}\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}}%
\DeclareOption{FTMstudentthesis}{\def\optFTMstudentthesis{x}\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}}%
%
% Module and style options:
% ----------------------------
\DeclareOption{optHelvetica}{\def\optHelvetica{x}}%
\DeclareOption{optArial}{\def\optArial{x}}%
\DeclareOption{optCharter}{\def\optCharter{x}}%
\DeclareOption{optComputerModern}{\def\optComputerModern{x}}%
\DeclareOption{optCharterMath}{\def\optCharterMath{x}}%
\DeclareOption{optComputerModernMath}{\def\optComputerModernMath{x}}%
\DeclareOption{optGerman}{\def\optGerman{x}}%
\DeclareOption{optEnglish}{\def\optEnglish{x}}%
\DeclareOption{optRGB}{\def\optRGB{x}}%
\DeclareOption{optCMYK}{\def\optCMYK{x}}%
\DeclareOption{optGray}{\def\optGray{x}}%
\DeclareOption{optMonochrome}{\def\optMonochrome{x}}%
\DeclareOption{optTikzExternalize}{\def\optTikzExternalize{x}}%
\DeclareOption{optLeftEquations}{\def\optLeftEquations{x}}%
\DeclareOption{optCenterEquations}{\def\optCenterEquations{x}}%
\DeclareOption{optAfour}{\def\optAfour{x}}%
\DeclareOption{optAzero}{\def\optAzero{x}}%
\DeclareOption{optBeamerClassicFormat}{\def\optBeamerClassicFormat{x}}%
\DeclareOption{optBeamerWideFormat}{\def\optBeamerWideFormat{x}}%
\DeclareOption{optExzellenz}{\def\optExzellenz{x}}%
\DeclareOption{optBiber}{\def\optBiber{x}}%
\DeclareOption{optBibtex}{\def\optBibtex{x}}%
\DeclareOption{optBibstyleNumeric}{\def\optBibstyleNumeric{x}}%
\DeclareOption{optBibstyleAlphabetic}{\def\optBibstyleAlphabetic{x}}%
\DeclareOption{optBibstyleAuthorYear}{\def\optBibstyleAuthorYear{x}}%
\DeclareOption{optHideTodos}{\def\optHideTodos{x}}%
\DeclareOption{optHideAnnotations}{\def\optHideAnnotations{x}}%
\DeclareOption{optGroupedAbbreviation}{\def\optGroupedAbbreviation{x}}%
%
% End of option processing
% ------------------------
\ProcessOptions\relax% End of option declaration
%
% Processing module dependencies:
% -------------------------------
\ifdefined\optFTMfont% Automatic loading dependencies of module FTMfont
	\def\optFTMcore{x}%
\else\fi%
\ifdefined\optFTMlang% Automatic loading dependencies of module FTMlang
	\def\optFTMcore{x}%
\else\fi%
\ifdefined\optFTMcolor% Automatic loading dependencies of module FTMcolor
	\def\optFTMcore{x}%
\else\fi%
\ifdefined\optFTMtikz% Automatic loading dependencies of module FTMtikz
	\def\optFTMcore{x}%
\else\fi%
\ifdefined\optFTMlogo% Automatic loading dependencies of module FTMlogo
	\def\optFTMcore{x}%
	\def\optFTMfont{x}%
	\def\optFTMcolor{x}%
	\def\optFTMlang{x}%
	\def\optFTMtikz{x}%
\else\fi%
\ifdefined\optFTMmath% Automatic loading dependencies of module FTMmath
	\def\optFTMcore{x}%
\else\fi%
\ifdefined\optFTMlayout% Automatic loading dependencies of module FTMlayout
	\def\optFTMcore{x}%
	\def\optFTMcolor{x}%
	\def\optFTMtikz{x}%
	\def\optFTMlogo{x}%
\else\fi%
\ifdefined\optFTMbiblio% Automatic loading dependencies of module FTMbiblio
	\def\optFTMcore{x}%
	\def\optFTMlang{x}%
\else\fi%
\ifdefined\optFTMnames% Automatic loading dependencies of module FTMnames
	\def\optFTMcore{x}%
\else\fi%
\ifdefined\optFTMutils% Automatic loading dependencies of module FTMutils
	\def\optFTMcore{x}%
	\def\optFTMlang{x}%
	\def\optFTMcolor{x}%
\else\fi%
\ifdefined\optFTMref% Automatic loading dependencies of module FTMref
	\def\optFTMcore{x}%
	\def\optFTMlang{x}%
	\def\optFTMcolor{x}%
\else\fi%
%
% Check number of selected styles (for 0: auto-select FTMempty as style (without explicit module selection))
%                                 (for 1: select this style and load ALL modules)
%                                 (for >1: throw error)
\newcounter{SelectedStyles}% Stores the number of selected styles
\ifdefined\optFTMdocumentation\stepcounter{SelectedStyles}\else\fi% Increase the counter by one...
\ifdefined\optFTMphdthesis\stepcounter{SelectedStyles}\else\fi% Increase the counter by one...
\ifdefined\optFTMstudentthesis\stepcounter{SelectedStyles}\else\fi% Increase the counter by one...
\ifnum\value{SelectedStyles}=0%
%   Load default style
	\def\optFTMempty{x}%
\else\fi%
\ifnum\value{SelectedStyles}=1%
%   Load ALL modules
	\def\optFTMcore{x}%
	\def\optFTMfont{x}%
	\def\optFTMlang{x}%
	\def\optFTMcolor{x}%
	\def\optFTMtikz{x}%
	\def\optFTMlogo{x}%
	\def\optFTMmath{x}%
	\def\optFTMlayout{x}%
	\def\optFTMbiblio{x}%
	\def\optFTMnames{x}%
	\def\optFTMutils{x}%
	\def\optFTMref{x}%
\else\fi%
\ifnum\value{SelectedStyles}>1%
%   Throw error
	\typeout{! Please select only ONE style.}%
\else\fi%
%
% Check number of selected modules (for 0: load ALL modules)
\newcounter{SelectedModules}% Stores the number of selected modules
\ifdefined\optFTMcore\stepcounter{SelectedModules}\else\fi% Increase the counter by one...
\ifdefined\optFTMfont\stepcounter{SelectedModules}\else\fi% Increase the counter by one...
\ifdefined\optFTMlang\stepcounter{SelectedModules}\else\fi% Increase the counter by one...
\ifdefined\optFTMcolor\stepcounter{SelectedModules}\else\fi% Increase the counter by one...
\ifdefined\optFTMtikz\stepcounter{SelectedModules}\else\fi% Increase the counter by one...
\ifdefined\optFTMlogo\stepcounter{SelectedModules}\else\fi% Increase the counter by one...
\ifdefined\optFTMmath\stepcounter{SelectedModules}\else\fi% Increase the counter by one...
\ifdefined\optFTMlayout\stepcounter{SelectedModules}\else\fi% Increase the counter by one...
\ifdefined\optFTMbiblio\stepcounter{SelectedModules}\else\fi% Increase the counter by one...
\ifdefined\optFTMnames\stepcounter{SelectedModules}\else\fi% Increase the counter by one...
\ifdefined\optFTMutils\stepcounter{SelectedModules}\else\fi% Increase the counter by one...
\ifdefined\optFTMref\stepcounter{SelectedModules}\else\fi% Increase the counter by one...
\ifnum\value{SelectedModules}=0%
%   Load ALL modules
	\def\optFTMcore{x}%
	\def\optFTMfont{x}%
	\def\optFTMlang{x}%
	\def\optFTMcolor{x}%
	\def\optFTMtikz{x}%
	\def\optFTMlogo{x}%
	\def\optFTMmath{x}%
	\def\optFTMlayout{x}%
	\def\optFTMbiblio{x}%
	\def\optFTMnames{x}%
	\def\optFTMutils{x}%
	\def\optFTMref{x}%
\else\fi%
%
%
%###################################################################################################
%--- BASE CLASS LOADING ----------------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMdocumentation\LoadClass[11pt,a4paper,oneside,fleqn]{book}\else\fi%
\ifdefined\optFTMphdthesis\LoadClass[11pt,a4paper,twoside]{book}\else\fi%
\ifdefined\optFTMstudentthesis\LoadClass[11pt,a4paper,twoside,fleqn]{book}\else\fi%
%
%
%###################################################################################################
%--- BEGIN MODULE FTMcore --------------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMcore% Start-check if module FTMcore is enabled
%
% >>> CONTENTS OF FILE source/TUM/Modules/TUMcore.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%================
%--- Packages ---
%================
\PassOptionsToPackage{utf8}{inputenc}%  sets input encoding to UTF-8
\RequirePackage{inputenc}%
\RequirePackage{etoolbox}%              for parsing conditional expressions
\RequirePackage{xparse}%                allows advanced command definitions
\RequirePackage{silence}%               for suppressing warnings
%
%
%=========================
%--- Warning Filtering ---
%=========================
\WarningFilter{biblatex}{Patching footnotes failed}% occurs with biblatex and beamer class
%
%
%=================
%--- Debugging ---
%=================
% Printing misc information
\def\FTMcoreLogInfo#1{\typeout{#1.}}%
%
% Printing warnings
\def\FTMcoreLogWarning#1{\typeout{LaTeX Warning: #1 on input line \the\inputlineno.}}%
%
% Printing errors
\def\FTMcoreLogError#1{\typeout{! #1.}}%
%
%
%==========================
%--- Control Structures ---
%==========================
\newcommand{\FTMcoreRepetition}[2]{\newcount\Step\Step=0\loop\ifnum\Step<#1\advance \Step by 1 {#2}\repeat}%
%
%
%============
%--- Misc ---
%============
% Suppress warning produced after including special PDF's (only use this command, if it is actually defined (since pdftex 1.40.15))
\begingroup\expandafter\expandafter\expandafter\endgroup%
\expandafter\ifx\csname pdfsuppresswarningpagegroup\endcsname\relax%
\else\pdfsuppresswarningpagegroup=1\relax\fi%
%
%
% >>> CONTENTS OF FILE source/FTM/Modules/FTMcore.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%================
%--- Packages ---
%================
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Begin FTM figures and tables
\RequirePackage{longtable}%
\RequirePackage{subcaption}%
\RequirePackage{tabularx}%
\RequirePackage{booktabs}% lines in tables
\setlength\heavyrulewidth{1.5pt} % thickness of toprule and bottomrule
\ifdefined\optFTMstudentthesis%
	\RequirePackage{multirow}% add rows and columns together
	\RequirePackage{floatrow}%
	\RequirePackage{placeins}%
	\DeclareFloatFont{tablefont}{\footnotesize}%
	\DeclareFloatVCode{objectSkip-6}{\vspace{-6pt}}%
	\DeclareFloatVCode{objectSkip0}{\vspace{0pt}}%
	\DeclareFloatVCode{objectSkip6}{\vspace{6pt}}%
	\DeclareFloatVCode{objectSkip12}{\vspace{12pt}}%
	\floatsetup[table]{style=plaintop, font={sf,footnotesize}, capposition=top, objectset=centering, margins=centering, justification=centering, captionskip=6pt, precode=objectSkip6, postcode=objectSkip0}%
	\floatsetup[figure]{style=plain, font={sf,footnotesize}, capposition=bottom, objectset=centering, margins=centering, justification=centering, captionskip=6pt, precode=objectSkip6, postcode=objectSkip0}%
%
	\RequirePackage{enumitem}%
	\setlist[itemize,1]{labelsep=\dimexpr 0.5cm, leftmargin=\dimexpr 1.27cm, rightmargin=\dimexpr 1cm, parsep=\dimexpr 6pt, topsep=\dimexpr 0pt, itemsep=\dimexpr 1pt}%
	\setlist[enumerate,1]{labelsep=\dimexpr 0.25cm, leftmargin=\dimexpr 1.27cm, rightmargin=\dimexpr 1cm, parsep=\dimexpr 6pt, topsep=\dimexpr 0pt, itemsep=\dimexpr 1pt}%
	\RequirePackage{array}%
	\newcolumntype{M}[1]{>{\centering\let\newline\\\arraybackslash}m{#1}}%
\else%
	\ifdefined\optFTMphdthesis%
		\RequirePackage{multirow}% add rows and columns together
		\RequirePackage{floatrow}%
		\RequirePackage{placeins}%
		\DeclareFloatFont{tablefont}{\footnotesize}%
		\DeclareFloatVCode{objectSkip-6}{\vspace{-6pt}}%
		\DeclareFloatVCode{objectSkip0}{\vspace{0pt}}%
		\DeclareFloatVCode{objectSkip6}{\vspace{6pt}}%
		\DeclareFloatVCode{objectSkip12}{\vspace{12pt}}%
		\floatsetup[table]{style=plaintop, font={sf,footnotesize}, capposition=top, objectset=centering, margins=centering, justification=centering, captionskip=6pt, precode=objectSkip6, postcode=objectSkip0}%
		\floatsetup[figure]{style=plain, font={sf,footnotesize}, capposition=bottom, objectset=centering, margins=centering, justification=centering, captionskip=6pt, precode=objectSkip6, postcode=objectSkip0}%
%
		\RequirePackage{enumitem}%
		\setlist[itemize,1]{labelsep=\dimexpr 0.5cm, leftmargin=\dimexpr 1.27cm, rightmargin=\dimexpr 1cm, parsep=\dimexpr 6pt, topsep=\dimexpr 0pt, itemsep=\dimexpr 1pt}%
		\setlist[enumerate,1]{labelsep=\dimexpr 0.25cm, leftmargin=\dimexpr 1.27cm, rightmargin=\dimexpr 1cm, parsep=\dimexpr 6pt, topsep=\dimexpr 0pt, itemsep=\dimexpr 1pt}%
		\RequirePackage{array}%
		\newcolumntype{M}[1]{>{\centering\let\newline\\\arraybackslash}m{#1}}%
	\else%
		\RequirePackage{float}%
\fi%
\fi%
%
%
\ifdefined\optFTMstudentthesis
	\DeclareCaptionLabelSeparator{FTMlabelsep}{:\quad}
	\DeclareCaptionLabelSeparator{FTMlabelsepSub}{\quad}
	\captionsetup{
		figurewithin=chapter,
		tablewithin=chapter
	}
	\captionsetup[table]{
		format=hang,
		width=0.9\textwidth,
		singlelinecheck=true,
		justification=justified,
		skip=6pt,
		font={sf,footnotesize},
		labelfont={sf,footnotesize},
		labelsep=FTMlabelsep
	}%
	% -- Caption-Styling Bilder:
	\captionsetup[figure]{
		format=hang,
		width=0.9\textwidth,
		singlelinecheck=true,
		justification=justified,
		skip=6pt,
		font={sf, footnotesize},
		labelfont={sf, footnotesize},
		labelsep=FTMlabelsep
	}
	% -- Caption-Styling Bilder:
	\captionsetup[subfigure]{
		format=hang,
		width=0.9\textwidth,
		singlelinecheck=true,
		justification=justified,
		skip=6pt,
		font={sf, footnotesize},
		labelfont={sf, footnotesize},
		labelsep=FTMlabelsepSub
	}
	\captionsetup[subtable]{
		format=hang,
		width=0.9\textwidth,
		singlelinecheck=true,
		justification=justified,
		skip=6pt,
		font={sf, footnotesize},
		labelfont={sf, footnotesize},
		labelsep=FTMlabelsepSub
	}
	% -- Caption-Styling Listing:
	\captionsetup[lstlisting]{
		format=hang,
		width=0.9\textwidth,
		singlelinecheck=true,
		justification=justified,
		skip=6pt,
		font={sf, footnotesize},
		labelfont={sf, footnotesize},
		labelsep=FTMlabelsep
	}%
\else%
	\ifdefined\optFTMphdthesis%
		\DeclareCaptionLabelSeparator{FTMlabelsep}{:\quad}
		\captionsetup{
			figurewithin=chapter,
			tablewithin=chapter
		}
		\captionsetup[table]{
			format=hang,
			width=0.9\textwidth,
			singlelinecheck=true,
			justification=justified,
			skip=6pt,
			font={sf,footnotesize},
			labelfont={sf,footnotesize},
			labelsep=FTMlabelsep
		}%
		% -- Caption-Styling Bilder:
		\captionsetup[figure]{
			format=hang,
			width=0.9\textwidth,
			singlelinecheck=true,
			justification=justified,
			skip=6pt,
			font={sf, footnotesize},
			labelfont={sf, footnotesize},
			labelsep=FTMlabelsep
		}
		% -- Caption-Styling Listing:
		\captionsetup[lstlisting]{
			format=hang,
			width=0.9\textwidth,
			singlelinecheck=true,
			justification=justified,
			skip=6pt,
			font={sf, footnotesize},
			labelfont={sf, footnotesize},
			labelsep=FTMlabelsep
		}%
\fi%
\fi%
%
% End FTM figures and tables
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%
\else\fi% End-check if module FTMcore is enabled
%###################################################################################################
%--- END MODULE FTMcore ----------------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- BEGIN MODULE FTMfont --------------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMfont% Start-check if module FTMfont is enabled
%
% >>> CONTENTS OF FILE source/TUM/Modules/TUMfont.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%===============================
%--- Default Option handling ---
%===============================
% Text: Use Helvetiva as default, if no font has been selected
% -----
\ifdefined\optHelvetica\else%
\ifdefined\optArial\else%
\ifdefined\optCharter\else%
\ifdefined\optComputerModern\else%
	\def\optHelvetica{x}%
\fi%
\fi%
\fi%
\fi%
%
% Math: Use Charter as default, if no font has been selected
% -----
\ifdefined\optCharterMath\else%
\ifdefined\optComputerModernMath\else%
	\def\optCharterMath{x}%
\fi%
\fi%
%
%
%================
%--- Packages ---
%================
\PassOptionsToPackage{T1}{fontenc}%                     Use T1 font encoding (necessary for correct hyphenation of german language)
\RequirePackage{fontenc}%
\RequirePackage{helvet}%                                Load Helvetica font (very similar to Arial and TUMNeueHelvetica)
\ifdefined\optArial%
	\RequirePackage{uarial}%                            Load URW Arial font
\fi%
\ifdefined\optComputerModernMath%
	% Attention: to keep the math font as Computer Modern (default), we MUST NOT load the mathdesign package
	\usepackage{charter}%                               Load Charter font for text only (math remains Computer Modern)
\else%
	\PassOptionsToPackage{expert,charter,cal=cmcal}{mathdesign}%  Load Charter font for text and math (option expert to prevent "fake small capitals - fsc") (option cal=cmcal to prevent overwriting of caligraphic symbols)
	\RequirePackage{mathdesign}%
\fi%
\ifdefined\optComputerModern%
	\renewcommand{\sfdefault}{cmss}%                    Set Computer Modern as default Sans Serif font
	\renewcommand{\rmdefault}{cmr}%                     Set Computer Modern as default Roman font
\else%
	\ifdefined\optHelvetica%
		\renewcommand{\sfdefault}{phv}%                 Set Helvetica as default Sans Serif font
	\fi%
	\ifdefined\optArial%
		\renewcommand{\sfdefault}{ua1}%                 Set Arial as default Sans Serif font
	\fi%
	\ifdefined\optCharter%
		\renewcommand{\sfdefault}{phv}%                 Set Helvetica as default Sans Serif font (Charter does not specify sans serif styles)
	\fi%
	\renewcommand{\rmdefault}{bch}%                     Set Charter as default Roman font (Helvetica and Arial do not specify roman styles)
\fi
\renewcommand{\ttdefault}{cmtt}%                        Set Computer Modern as default Typewriter font
\RequirePackage{anyfontsize}%                           Allow any font size by scaling
%
%
%================
%--- Commands ---
%================
% Select font default style
% -------------------------
\ifdefined\optHelvetica%
	\renewcommand{\familydefault}{\sfdefault}\sffamily%  use sans serif type as default
\fi%
\ifdefined\optArial%
	\renewcommand{\familydefault}{\sfdefault}\sffamily%  use sans serif type as default
\fi%
\ifdefined\optCharter%
	\renewcommand{\familydefault}{\rmdefault}\rmfamily%  use roman type as default
\fi%
\ifdefined\optComputerModern%
	\renewcommand{\familydefault}{\rmdefault}\rmfamily%  use roman type as default
\fi%
%
% Font sizes
% ----------
\providecommand{\@ptsize}{11}% define ptsize if not already defined
%
% Font size 8
\newcommand{\FTMfontSetDocumentFontSizeVIII}{%
	\renewcommand\@ptsize{8}%
	\renewcommand\tiny{\@setfontsize\tiny{4.5}{5}}%
	\renewcommand\scriptsize{\@setfontsize\scriptsize{4.5}{5}}%
	\renewcommand\footnotesize{\@setfontsize\footnotesize{5}{6}}%
	\renewcommand\small{\@setfontsize\small{7}{8}}%
	\renewcommand\normalsize{\@setfontsize\normalsize{8}{9.5}}%
	\renewcommand\large{\@setfontsize\large{9}{11}}%
	\renewcommand\Large{\@setfontsize\Large{10}{12}}%
	\renewcommand\LARGE{\@setfontsize\LARGE{12}{14}}%
	\renewcommand\huge{\@setfontsize\huge{14.4}{18}}%
	\renewcommand\Huge{\@setfontsize\Huge{17}{22}}%
}%
% Font size 9
\newcommand{\FTMfontSetDocumentFontSizeIX}{%
	\renewcommand\@ptsize{9}%
	\renewcommand\tiny{\@setfontsize\tiny{4.5}{5}}%
	\renewcommand\scriptsize{\@setfontsize\scriptsize{5}{6}}%
	\renewcommand\footnotesize{\@setfontsize\footnotesize{7}{8}}%
	\renewcommand\small{\@setfontsize\small{8}{9.5}}%
	\renewcommand\normalsize{\@setfontsize\normalsize{9}{11}}%
	\renewcommand\large{\@setfontsize\large{10}{12}}%
	\renewcommand\Large{\@setfontsize\Large{12}{14}}%
	\renewcommand\LARGE{\@setfontsize\LARGE{14.4}{18}}%
	\renewcommand\huge{\@setfontsize\huge{17}{22}}%
	\renewcommand\Huge{\@setfontsize\Huge{20}{25}}%
}%
% Font size 10
\newcommand{\FTMfontSetDocumentFontSizeX}{%
	\renewcommand\@ptsize{10}%
	\renewcommand\tiny{\@setfontsize\tiny{5}{6}}%
	\renewcommand\scriptsize{\@setfontsize\scriptsize{7}{8}}%
	\renewcommand\footnotesize{\@setfontsize\footnotesize{8}{9.5}}%
	\renewcommand\small{\@setfontsize\small{9}{11}}%
	\renewcommand\normalsize{\@setfontsize\normalsize{10}{12}}%
	\renewcommand\large{\@setfontsize\large{12}{14}}%
	\renewcommand\Large{\@setfontsize\Large{14.4}{18}}%
	\renewcommand\LARGE{\@setfontsize\LARGE{17}{22}}%
	\renewcommand\huge{\@setfontsize\huge{20}{25}}%
	\renewcommand\Huge{\@setfontsize\Huge{25}{30}}%
}%
% Font size 11
\newcommand{\FTMfontSetDocumentFontSizeXI}{%
	\renewcommand\@ptsize{11}%
	\renewcommand\tiny{\@setfontsize\tiny{6}{7}}%
	\renewcommand\scriptsize{\@setfontsize\scriptsize{8}{9.5}}%
	\renewcommand\footnotesize{\@setfontsize\footnotesize{9}{11}}%
	\renewcommand\small{\@setfontsize\small{10}{12}}%
	\renewcommand\normalsize{\@setfontsize\normalsize{10.95}{13.6}}%
	\renewcommand\large{\@setfontsize\large{12}{14}}%
	\renewcommand\Large{\@setfontsize\Large{14.4}{18}}%
	\renewcommand\LARGE{\@setfontsize\LARGE{17}{22}}%
	\renewcommand\huge{\@setfontsize\huge{20}{25}}%
	\renewcommand\Huge{\@setfontsize\Huge{25}{30}}%
}
% Font size 12
\newcommand{\FTMfontSetDocumentFontSizeXII}{%
	\renewcommand\@ptsize{12}%
	\renewcommand\tiny{\@setfontsize\tiny{6}{7}}%
	\renewcommand\scriptsize{\@setfontsize\scriptsize{8}{9.5}}%
	\renewcommand\footnotesize{\@setfontsize\footnotesize{10}{12}}%
	\renewcommand\small{\@setfontsize\small{10.95}{13.6}}%
	\renewcommand\normalsize{\@setfontsize\normalsize{12}{14.5}}%
	\renewcommand\large{\@setfontsize\large{14.4}{18}}%
	\renewcommand\Large{\@setfontsize\Large{17}{22}}%
	\renewcommand\LARGE{\@setfontsize\LARGE{20}{25}}%
	\renewcommand\huge{\@setfontsize\huge{25}{30}}%
	\renewcommand\Huge{\@setfontsize\Huge{25}{30}}%
}%
% Font size 14
\newcommand{\FTMfontSetDocumentFontSizeXIV}{%
	\renewcommand\@ptsize{14}%
	\renewcommand\tiny{\@setfontsize\tiny{7}{8.4}}%
	\renewcommand\scriptsize{\@setfontsize\scriptsize{9.8}{11.2}}%
	\renewcommand\footnotesize{\@setfontsize\footnotesize{11.2}{13.3}}%
	\renewcommand\small{\@setfontsize\small{12.6}{15.4}}%
	\renewcommand\normalsize{\@setfontsize\normalsize{14}{16.8}}%
	\renewcommand\large{\@setfontsize\large{16.8}{19.6}}%
	\renewcommand\Large{\@setfontsize\Large{20.2}{25.2}}%
	\renewcommand\LARGE{\@setfontsize\LARGE{23.8}{30.8}}%
	\renewcommand\huge{\@setfontsize\huge{28}{35}}%
	\renewcommand\Huge{\@setfontsize\Huge{35}{42}}%
}%
% Font size 16
\newcommand{\FTMfontSetDocumentFontSizeXVI}{%
	\renewcommand\@ptsize{16}%
	\renewcommand\tiny{\@setfontsize\tiny{8}{9.5}}%
	\renewcommand\scriptsize{\@setfontsize\scriptsize{10.95}{13.6}}%
	\renewcommand\footnotesize{\@setfontsize\footnotesize{13}{15}}%
	\renewcommand\small{\@setfontsize\small{14.4}{18}}%
	\renewcommand\normalsize{\@setfontsize\normalsize{16}{19}}%
	\renewcommand\large{\@setfontsize\large{19}{22}}%
	\renewcommand\Large{\@setfontsize\Large{23}{29}}%
	\renewcommand\LARGE{\@setfontsize\LARGE{27}{35}}%
	\renewcommand\huge{\@setfontsize\huge{32}{40}}%
	\renewcommand\Huge{\@setfontsize\Huge{40}{48}}%
}%
% Font size 18
\newcommand{\FTMfontSetDocumentFontSizeXVIII}{%
	\renewcommand\@ptsize{18}%
	\renewcommand\tiny{\@setfontsize\tiny{9}{11}}%
	\renewcommand\scriptsize{\@setfontsize\scriptsize{12.6}{14.4}}%
	\renewcommand\footnotesize{\@setfontsize\footnotesize{14.4}{17}}%
	\renewcommand\small{\@setfontsize\small{16.2}{20}}%
	\renewcommand\normalsize{\@setfontsize\normalsize{18}{21.6}}%
	\renewcommand\large{\@setfontsize\large{21.6}{25}}%
	\renewcommand\Large{\@setfontsize\Large{26}{32}}%
	\renewcommand\LARGE{\@setfontsize\LARGE{31}{40}}%
	\renewcommand\huge{\@setfontsize\huge{36}{45}}%
	\renewcommand\Huge{\@setfontsize\Huge{45}{54}}%
}%
% Font size 20
\newcommand{\FTMfontSetDocumentFontSizeXX}{%
	\renewcommand\@ptsize{20}%
	\renewcommand\tiny{\@setfontsize\tiny{10}{12}}%
	\renewcommand\scriptsize{\@setfontsize\scriptsize{14}{16}}%
	\renewcommand\footnotesize{\@setfontsize\footnotesize{16}{19}}%
	\renewcommand\small{\@setfontsize\small{18}{22}}%
	\renewcommand\normalsize{\@setfontsize\normalsize{20}{24}}%
	\renewcommand\large{\@setfontsize\large{24}{28}}%
	\renewcommand\Large{\@setfontsize\Large{28.8}{36}}%
	\renewcommand\LARGE{\@setfontsize\LARGE{34}{44}}%
	\renewcommand\huge{\@setfontsize\huge{40}{50}}%
	\renewcommand\Huge{\@setfontsize\Huge{50}{60}}%
}%
% Font size 44
\newcommand{\FTMfontSetDocumentFontSizeXLIV}{%
	\renewcommand\@ptsize{44}%
	\renewcommand\tiny{\@setfontsize\tiny{22}{26}}%
	\renewcommand\scriptsize{\@setfontsize\scriptsize{28}{35}}%
	\renewcommand\footnotesize{\@setfontsize\footnotesize{35}{42}}%
	\renewcommand\small{\@setfontsize\small{40}{48}}%
	\renewcommand\normalsize{\@setfontsize\normalsize{44}{53}}%
	\renewcommand\large{\@setfontsize\large{53}{62}}%
	\renewcommand\Large{\@setfontsize\Large{63}{79}}%
	\renewcommand\LARGE{\@setfontsize\LARGE{75}{97}}%
	\renewcommand\huge{\@setfontsize\huge{88}{110}}%
	\renewcommand\Huge{\@setfontsize\Huge{110}{132}}%
}%
%
%
% >>> CONTENTS OF FILE source/FTM/Modules/FTMfont.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%
%
%%%%%%%%%%%%%%
%--------change font------------
%%%%%%%%%%%%%%
%
\ifdefined\optFTMstudentthesis%
	\RequirePackage{uarial}%
	\RequirePackage[tracking=normalfont, letterspace = 0]{microtype}%
	%\renewcommand{\familydefault}{\sfdefault}%
\else%
	\ifdefined\optFTMphdthesis%
		\RequirePackage{uarial}%
		\RequirePackage[tracking=normalfont, letterspace = 0]{microtype}%
		%\renewcommand{\familydefault}{\sfdefault}%
		\else%
		\fi%
\fi%
%
%
\else\fi% End-check if module FTMfont is enabled
%###################################################################################################
%--- END MODULE FTMfont ----------------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- BEGIN MODULE FTMlang --------------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMlang% Start-check if module FTMlang is enabled
%
% >>> CONTENTS OF FILE source/TUM/Modules/TUMlang.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%===============================
%--- Default Option handling ---
%===============================
% Use german as default, if no language has been selected
\ifdefined\optGerman\else%
\ifdefined\optEnglish\else%
	\def\optGerman{x}%
\fi%
\fi%
%
%
%================
%--- Packages ---
%================
\ifdefined\optGerman%
	\PassOptionsToPackage{english,ngerman}{babel}%
\else\fi%
\ifdefined\optEnglish%
	\PassOptionsToPackage{ngerman,english}{babel}%
\else\fi%
\RequirePackage{babel}%
\RequirePackage{csquotes}%
%
%
%================
%--- Commands ---
%================
% Switch language
% ---------------
\newcommand{\FTMlangSwitchToGerman}{%
	\def\optGerman{x}%
	\undef\optEnglish%
	\selectlanguage{ngerman}%
}%
\newcommand{\FTMlangSwitchToEnglish}{%
	\def\optEnglish{x}%
	\undef\optGerman%
	\selectlanguage{english}%
}%
%
% Auto-select language
% --------------------
\newcommand{\FTMlangGerEng}[2]{\ifdefined\optGerman#1\else\fi\ifdefined\optEnglish#2\else\fi}%
\newcommand{\FTMlangForceGerman}[1]{%
	\ifdefined\optEnglish%
		\FTMlangSwitchToGerman%
		#1%
		\FTMlangSwitchToEnglish%
	\else\fi%
	\ifdefined\optGerman%
		#1%
	\else\fi%
}%
\newcommand{\FTMlangForceEnglish}[1]{%
	\ifdefined\optGerman%
		\FTMlangSwitchToEnglish%
		#1%
		\FTMlangSwitchToGerman%
	\else\fi%
	\ifdefined\optEnglish%
		#1%
	\else\fi%
}%
%
\newcommand{\nospace}[0]{%
	\ifdefined\optGerman%
		\negmedspace
	\else\fi%
}%
%
%
%===================
%--- Definitions ---
%===================
% TUM
% ---
\def\FTMlangTUM{\FTMlangGerEng{Technische Universität München}{Technical University of Munich}}%
%
% Department
% ----------
\def\FTMlangDepartment{\FTMlangGerEng{Fakultät für Maschinenwesen}{Department of Mechanical Engineering}}%
%
% Chairs
% ------
\def\FTMlangChairAER{\FTMlangGerEng{Lehrstuhl für Aerodynamik und Strömungsmechanik}{Chair of Aerodynamics and Fluid Mechanics}}%
\def\FTMlangChairVIB{\FTMlangGerEng{Lehrstuhl für Akustik mobiler Systeme}{Chair of Vibroacoustics of Vehicles and Machines}}%
\def\FTMlangChairAM{\FTMlangGerEng{Lehrstuhl für Angewandte Mechanik}{Chair of Applied Mechanics}}%
\def\FTMlangChairAPT{\FTMlangGerEng{Lehrstuhl für Anlagen- und Prozesstechnik}{Chair of Plant and Process Technology}}%
\def\FTMlangChairAIS{\FTMlangGerEng{Lehrstuhl für Automatisierung und Informationssysteme}{Chair of Automation and Information Systems}}%
\def\FTMlangChairIWB{\FTMlangGerEng{Institut für Werkzeugmaschinen und Betriebswissenschaften}{Institute for Machine Tools and Industrial Management}}%
\def\FTMlangChairBVT{\FTMlangGerEng{Lehrstuhl für Bioverfahrenstechnik}{Chair of Biochemical Engineering}}%
\def\FTMlangChairLCC{\FTMlangGerEng{Lehrstuhl für Carbon Composites}{Chair of Carbon Composites}}%
\def\FTMlangChairLES{\FTMlangGerEng{Lehrstuhl für Energiesysteme}{Chair of Energy Systems}}%
\def\FTMlangChairLFE{\FTMlangGerEng{Lehrstuhl für Ergonomie}{Chair of Ergonomics}}%
\def\FTMlangChairFTM{\FTMlangGerEng{Lehrstuhl für Fahrzeugtechnik}{Chair of Automotive Technology}}%
\def\FTMlangChairFSD{\FTMlangGerEng{Lehrstuhl für Flugsystemdynamik}{Chair of Flight System Dynamics}}%
\def\FTMlangChairFML{\FTMlangGerEng{Lehrstuhl für Fördertechnik Materialfluss Logistik / Technische Logistik}{Chair of Materials Handling, Material Flow, Logistics / Logistics Engineering}}%
\def\FTMlangChairLHT{\FTMlangGerEng{Lehrstuhl für Hubschraubertechnologie}{Chair of Helicopter Technology}}%
\def\FTMlangChairPKM{\FTMlangGerEng{Professur für Kontinuumsmechanik}{Associate Professorship of Continuum Mechanics}}%
\def\FTMlangChairLLB{\FTMlangGerEng{Lehrstuhl für Leichtbau}{Chair of Lightweight Structures}}%
\def\FTMlangChairLLS{\FTMlangGerEng{Lehrstuhl für Luftfahrtsysteme}{Chair of Aircraft Design}}%
\def\FTMlangChairFZG{\FTMlangGerEng{Lehrstuhl für Maschinenelemente}{Chair of Machine Elements}}%
\def\FTMlangChairMHPC{\FTMlangGerEng{Professur für Mechanik auf Höchstleistungsrechnern}{Associate Professorship of Mechanics and High Performance Computing}}%
\def\FTMlangChairLMT{\FTMlangGerEng{Lehrstuhl für Medizintechnik}{Chair of Medical Engineering}}%
\def\FTMlangChairLMM{\FTMlangGerEng{Lehrstuhl für Mikrotechnik und Medizingerätetechnik}{Chair of Micro Technology and Medical Device Technology}}%
\def\FTMlangChairLNT{\FTMlangGerEng{Lehrstuhl für Nukleartechnik}{Chair of Nuclear Technology}}%
\def\FTMlangChairLNM{\FTMlangGerEng{Lehrstuhl für Numerische Mechanik}{Chair of Computational Mechanics}}%
\def\FTMlangChairPMW{\FTMlangGerEng{Professur für Plasma-Material-Wechselwirkung}{Associate Professorship of Plasma Material Interaction}}%
\def\FTMlangChairPE{\FTMlangGerEng{Lehrstuhl für Produktentwicklung}{Chair of Product Development}}%
\def\FTMlangChairPTM{\FTMlangGerEng{Lehrstuhl für Produktion und Technik in der Medienbranche}{Chair of Production and Technology in Media}}%
\def\FTMlangChairLFA{\FTMlangGerEng{Lehrstuhl für Raumfahrtantriebe}{Chair of Space Propulsion}}%
\def\FTMlangChairLRT{\FTMlangGerEng{Lehrstuhl für Raumfahrttechnik}{Chair of Astronautics}}%
\def\FTMlangChairRT{\FTMlangGerEng{Lehrstuhl für Regelungstechnik}{Chair of Automatic Control}}%
\def\FTMlangChairSES{\FTMlangGerEng{Professur für Sichere Eingebettete Systeme}{Assistant Professorship of Safe Embedded Systems}}%
\def\FTMlangChairSPGM{\FTMlangGerEng{Professur für Sportgeräte und Sportmaterialien}{Associate Professorship of Sport Equipment and Materials}}%
\def\FTMlangChairTD{\FTMlangGerEng{Lehrstuhl für Thermodynamik}{Chair of Thermodynamics}}%
\def\FTMlangChairTFD{\FTMlangGerEng{Professur für Thermofluiddynamik}{Associate Professorship of Thermo-Fluid Dynamics}}%
\def\FTMlangChairUTG{\FTMlangGerEng{Lehrstuhl für Umformtechnik und Gießereiwesen}{Chair of Metal Forming and Casting}}%
\def\FTMlangChairLVK{\FTMlangGerEng{Lehrstuhl für Verbrennungskraftmaschinen}{Chair of Internal Combustion Engines}}%
\def\FTMlangChairWKM{\FTMlangGerEng{Lehrstuhl für Werkstoffkunde und Werkstoffmechanik}{Chair of Materials Science and Mechanics of Materials}}%
\def\FTMlangChairLWE{\FTMlangGerEng{Lehrstuhl für Windenergie}{Chair of Wind Energy}}%
\def\FTMlangChairZFP{\FTMlangGerEng{Lehrstuhl für Zerstörungsfreie Prüfung}{Chair of Non-Destructive Testing}}%
%
% Current chair
% -------------
\def\FTMlangChair{\FTMlangChairFTM}%
%
% Roles
% -----
\def\FTMlangresearchassistantMale{\FTMlangGerEng{wissenschaftlicher Mitarbeiter}{research assistant}}%
\def\FTMlangResearchassistantMale{\FTMlangGerEng{Wissenschaftlicher Mitarbeiter}{Research assistant}}%
\def\FTMlangResearchAssistantMale{\FTMlangGerEng{Wissenschaftlicher Mitarbeiter}{Research Assistant}}%
\def\FTMlangresearchassistantFemale{\FTMlangGerEng{wissenschaftliche Mitarbeiterin}{research assistant}}%
\def\FTMlangResearchassistantFemale{\FTMlangGerEng{Wissenschaftliche Mitarbeiterin}{Research assistant}}%
\def\FTMlangResearchAssistantFemale{\FTMlangGerEng{Wissenschaftliche Mitarbeiterin}{Research Assistant}}%
\def\FTMlangtenuredprofessorMale{\FTMlangGerEng{Ordinarius}{tenured professor}}%
\def\FTMlangTenuredprofessorMale{\FTMlangGerEng{Ordinarius}{Tenured professor}}%
\def\FTMlangTenuredProfessorMale{\FTMlangGerEng{Ordinarius}{Tenured Professor}}%
\def\FTMlangtenuredprofessorFemale{\FTMlangGerEng{Ordinaria}{tenured professor}}%
\def\FTMlangTenuredprofessorFemale{\FTMlangGerEng{Ordinaria}{Tenured professor}}%
\def\FTMlangTenuredProfessorFemale{\FTMlangGerEng{Ordinaria}{Tenured Professor}}%
\def\FTMlangsupervisor{\FTMlangGerEng{Betreuer}{supervisor}}%
\def\FTMlangSupervisor{\FTMlangGerEng{Betreuer}{Supervisor}}%
\def\FTMlangsupervision{\FTMlangGerEng{Betreuung}{supervision}}%
\def\FTMlangSupervision{\FTMlangGerEng{Betreuung}{Supervision}}%
\def\FTMlangexaminer{\FTMlangGerEng{Prüfer}{examiner}}%
\def\FTMlangExaminer{\FTMlangGerEng{Prüfer}{Examiner}}%
%
% Student thesis
% --------------
\def\FTMlangbachelorsthesis{\FTMlangGerEng{Bachelorarbeit}{bachelor's thesis}}%
\def\FTMlangBachelorsthesis{\FTMlangGerEng{Bachelorarbeit}{Bachelor's thesis}}%
\def\FTMlangBachelorsThesis{\FTMlangGerEng{Bachelorarbeit}{Bachelor's Thesis}}%
\def\FTMlangsemesterthesis{\FTMlangGerEng{Semesterarbeit}{semester thesis}}%
\def\FTMlangSemesterthesis{\FTMlangGerEng{Semesterarbeit}{Semester thesis}}%
\def\FTMlangSemesterThesis{\FTMlangGerEng{Semesterarbeit}{Semester Thesis}}%
\def\FTMlangmastersthesis{\FTMlangGerEng{Masterarbeit}{master's thesis}}%
\def\FTMlangMastersthesis{\FTMlangGerEng{Masterarbeit}{Master's thesis}}%
\def\FTMlangMastersThesis{\FTMlangGerEng{Masterarbeit}{Master's Thesis}}%
\def\FTMlanginterdisciplinaryproject{\FTMlangGerEng{interdisziplinäres Projekt}{interdisciplinary project}}
\def\FTMlangInterdisciplinaryproject{\FTMlangGerEng{Interdisziplinäres Projekt}{Interdisciplinary project}}
\def\FTMlangInterdisciplinaryProject{\FTMlangGerEng{Interdisziplinäres Projekt}{Interdisciplinary Project}}
%
% Date and Time
% -------------
\def\FTMlangDate{\FTMlangGerEng{Datum}{Date}}%
%
\newcommand{\FTMlangMonth}[1]{%
	\ifdefined\optGerman\ifcase#1\or Januar\or Februar\or M\"arz\or April\or Mai\or Juni\or Juli\or August\or September\or Oktober\or November\or Dezember\fi\else\fi%
	\ifdefined\optEnglish\ifcase#1\or January\or February\or March\or April\or May\or June\or July\or August\or September\or October\or November\or December\fi\else\fi%
}%
\newcommand{\FTMlangMonthShort}[1]{%
	\ifdefined\optGerman\ifcase#1\or Jan\or Feb\or M\"ar\or Apr\or Mai\or Jun\or Jul\or Aug\or Sep\or Okt\or Nov\or Dez\fi\else\fi%
	\ifdefined\optEnglish\ifcase#1\or Jan\or Feb\or Mar\or Apr\or May\or Jun\or Jul\or Aug\or Sep\or Oct\or Nov\or Dec\fi\else\fi%
}%
\newcommand{\FTMlangmonth}[1]{%
	\ifdefined\optGerman\ifcase#1\or Januar\or Februar\or M\"arz\or April\or Mai\or Juni\or Juli\or August\or September\or Oktober\or November\or Dezember\fi\else\fi%
	\ifdefined\optEnglish\ifcase#1\or january\or february\or march\or april\or may\or june\or july\or august\or september\or october\or november\or december\fi\else\fi%
}%
\newcommand{\FTMlangmonthShort}[1]{%
	\ifdefined\optGerman\ifcase#1\or Jan\or Feb\or M\"ar\or Apr\or Mai\or Jun\or Jul\or Aug\or Sep\or Okt\or Nov\or Dez\fi\else\fi%
	\ifdefined\optEnglish\ifcase#1\or jan\or feb\or mar\or apr\or may\or jun\or jul\or aug\or sep\or oct\or nov\or dec\fi\else\fi%
}%
%
%
% >>> CONTENTS OF FILE source/FTM/Modules/FTMlang.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%
%
\def\FTMlangSupervisedBy{\FTMlangGerEng{Betreut von}{Supervised by}}%
\def\FTMlangSubmittedBy{\FTMlangGerEng{Eingereicht von}{Submitted by}}%
\def\FTMlangSubmittedOn{\FTMlangGerEng{Eingereicht am}{Submitted on}}%
\def\FTMlangScientificWorkForObtainingTheAcademicDegree{\FTMlangGerEng{Wissenschaftliche Arbeit zur Erlangung des Grades}{Scientific work for obtaining the academic degree}}%
\def\FTMlangProjectDescription{\FTMlangGerEng{Aufgabenstellung}{Project description}}%
\def\FTMlangAnnouncementDate{\FTMlangGerEng{Ausgabe}{Announcement date}}%
\def\FTMlangSubmissionDate{\FTMlangGerEng{Abgabe}{Submission date}}%
\def\FTMlangContentsName{\FTMlangGerEng{Inhaltsverzeichnis}{Contents}}%
\def\FTMlangAppendixName{\FTMlangGerEng{Anhang}{Appendix}}%
\def\FTMlangGlossaryName{\FTMlangGerEng{Abkürzungsverzeichnis}{List of Abbreviations}}%
\def\FTMlangFormulaSymbolsName{\FTMlangGerEng{Formelzeichen}{Formula Symbols}}%
\def\FTMlangFormulaSymbolsUnitName{\FTMlangGerEng{Einheit}{Unit}}%
\def\FTMlangFormulaSymbolsDescriptionName{\FTMlangGerEng{Beschreibung}{Description}}%
\def\FTMlangLiteratureName{\FTMlangGerEng{Literaturverzeichnis}{Bibliography}}%
\def\FTMlangLiteratureOwnName{\FTMlangGerEng{Eigene Veröffentlichungen}{Own Publications}}%
\def\FTMlangLiteratureAndName{\FTMlangGerEng{und}{and}}%
\def\FTMlangLiteratureEditorName{\FTMlangGerEng{Hrsg.}{ed.}}%
\def\FTMlangLiteratureVolumeName{\FTMlangGerEng{Bd.}{vol.}}%
\def\FTMlangLiteratureNumberName{\FTMlangGerEng{Rn.}{no.}}%
\def\FTMlangLiteratureOnlineDateSeperator{\FTMlangGerEng{.}{/}}%
\def\FTMlangLiteratureRepositoryName{\FTMlangGerEng{Rep.}{rep.}}%
\def\FTMlangLiteratureJournalsPeerReviewedName{\FTMlangGerEng{Zeitschriften; Scopus/Web of Science gelistet (peer-reviewed)}{Journals; Scopus/Web of Science listed (peer-reviewed)}}%
\def\FTMlangLiteratureConferencesPeriodicalPeerReviewedName{\FTMlangGerEng{Konferenzen, Magazine, etc.; Scopus/Web of Science gelistet (peer-reviewed)}{Conferences, Periodicals; Scopus/Web of Science listed (peer-reviewed)}}%
\def\FTMlangLiteraturePatentName{\FTMlangGerEng{Patente}{Patents}}%
\def\FTMlangLiteratureNotPeerReviewedName{\FTMlangGerEng{Zeitschriften, Konferenzen, Magazine, Berichte, Konferenzvorträge und -poster, etc.; nicht Scopus/Web of Science gelistet}{Journals, Conferences, Periodicals, Reports, Conference Proceedings and Poster, etc.; not Scopus/Web of Science listed}}%
\def\FTMlangLiteraturePeerReviewedNotRelevantName{\FTMlangGerEng{Nicht-dissertationsrelevante Veröffentlichungen; Scopus/Web of Science gelistet (peer-reviewed)}{Non-thesis-relevant publications; Scopus/Web of Science listed (peer-reviewed)}}%
\def\FTMlangLiteratureOpenSourceName{\FTMlangGerEng{Dissertationsrelevante Open-Source Software}{Thesis-relevant open-source software}}%
\def\FTMlangLiteratureStudentsThesisName{\FTMlangGerEng{Betreute Studienarbeiten}{Supervised Student's Thesis}}%
\def\FTMlangLiteratureStudentsThesisPrenote{\FTMlangGerEng{Folgende studentische Arbeiten entstanden im Rahmen der Dissertation unter der inhaltlichen, fachlichen und wissenschaftlichen Betreuung sowie unter maßgeblicher Anleitung des Autors. Im Folgenden sind die für diese Dissertation relevanten und in Bezug stehenden \mbox{Bachelor-,} Semester- und Masterarbeiten aufgeführt. Vielen Dank geht hier an die Bearbeiter für die umfangreiche Unterstützung im Rahmen dieses Forschungsprojekt.}{The following student theses were written within the framework of the dissertation under the supervision of the author in terms of content, technical and scientific support as well as under relevant guidance of the author. In the following, the bachelor, semester and master theses relevant and related to this dissertation are listed. Many thanks to the authors of these theses for their extensive support within the framework of this research project.}}%
\def\FTMlangLiteraturePriorPublicationsName{\FTMlangGerEng{Vorveröffentlichungsliste}{Prior Publications}}%
\def\FTMlangLiteraturePriorPublicationsPrenote{\FTMlangGerEng{Während der Anfertigung dieser Dissertation entstanden Veröffentlichungen und Studienar-beiten, in denen Teilaspekte dieser Arbeit vorgestellt wurden.}{During the development of this dissertation, publications and student theses were written in which partial aspects of this work were presented.}}%
%
\else\fi% End-check if module FTMlang is enabled
%###################################################################################################
%--- END MODULE FTMlang ----------------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- BEGIN MODULE FTMcolor -------------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMcolor% Start-check if module FTMcolor is enabled
%
% >>> CONTENTS OF FILE source/TUM/Modules/TUMcolor.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%===============================
%--- Default Option handling ---
%===============================
% Select rgb-model, if no option has been passed
\ifdefined\optRGB\else%
\ifdefined\optCMYK\else%
\ifdefined\optGray\else%
\ifdefined\optMonochrome\else%
	\def\optRGB{x}%
\fi%
\fi%
\fi%
\fi%
%
%
%================
%--- Packages ---
%================
% Select color model
\ifdefined\optRGB%
	\PassOptionsToPackage{rgb}{xcolor}%
\else\fi%
\ifdefined\optCMYK%
	\PassOptionsToPackage{cmyk}{xcolor}%
\else\fi%
\ifdefined\optGray%
	\PassOptionsToPackage{gray}{xcolor}%
\else\fi%
\ifdefined\optMonochrome%
	\PassOptionsToPackage{monochrome}{xcolor}%
\else\fi%
\RequirePackage{xcolor}%
%
%
%===================
%--- Definitions ---
%===================
% TUM colors
\ifdefined\optCMYK%
	% Primary Colors in CMYK
	\definecolor{TUMBlue}{cmyk}{1,0.43,0,0}%           Pantone 300
	\definecolor{TUMWhite}{cmyk}{0,0,0,0}%
	\definecolor{TUMBlack}{cmyk}{0,0,0,1}%
	% Secondary Colors in CMYK
	\definecolor{TUMBlue1}{cmyk}{1,0.57,0.12,0.7}%     Pantone 540
	\definecolor{TUMBlue2}{cmyk}{1,0.54,0.04,0.19}%    Pantone 301
	\definecolor{TUMGray1}{cmyk}{0,0,0,0.8}%
	\definecolor{TUMGray2}{cmyk}{0,0,0,0.5}%
	\definecolor{TUMGray3}{cmyk}{0,0,0,0.2}%
	% Accent Colors in CMYK
	\definecolor{TUMBlue3}{cmyk}{0.65,0.19,0.01,0.04}% Pantone 542
	\definecolor{TUMBlue4}{cmyk}{0.42,0.09,0,0}%       Pantone 283
	\definecolor{TUMIvory}{cmyk}{0.03,0.04,0.14,0.08}%
	\definecolor{TUMOrange}{cmyk}{0,0.65,0.95,0}%
	\definecolor{TUMGreen}{cmyk}{0.35,0,1,0.2}%
	%
	% Anniversary colors "150 Jahre culture of excellence" (for use in 2018 only)
	\definecolor{TUMAnniMustard}{cmyk}{12,18,85,0}%     Pantone 7405
	\definecolor{TUMAnniMustard2}{cmyk}{18,25,90,10}%   Pantone 103
	\definecolor{TUMAnniOrange}{cmyk}{0,40,100,0}%      Pantone 137
	\definecolor{TUMAnniOrange2}{cmyk}{0,50,100,0}%     Pantone 151
	\definecolor{TUMAnniGreen}{cmyk}{35,0,95,0}%        Pantone 382
	\definecolor{TUMAnniGreen2}{cmyk}{45,5,100,0}%      Pantone 376
	\definecolor{TUMAnniBlue}{cmyk}{45,0,3,0}%          Pantone 297
	\definecolor{TUMAnniBlue2}{cmyk}{60,0,0,0}%         Pantone 306
	\definecolor{TUMAnniPink}{cmyk}{0,55,30,0}%         Pantone 708
	\definecolor{TUMAnniPink2}{cmyk}{8,60,30,0}%        Pantone 702
\else%
	% Primary Colors in RGB
	\definecolor{TUMBlue}{RGB}{0,101,189}%      Pantone 300
	\definecolor{TUMWhite}{RGB}{255,255,255}%
	\definecolor{TUMBlack}{RGB}{0,0,0}%
	% Secondary Colors in RGB
	\definecolor{TUMBlue1}{RGB}{0,51,89}%       Pantone 540
	\definecolor{TUMBlue2}{RGB}{0,82,147}%      Pantone 301
	\definecolor{TUMGray1}{RGB}{51,51,51}%
	\definecolor{TUMGray2}{RGB}{127,127,127}%
	\definecolor{TUMGray3}{RGB}{204,204,204}%
	% Accent Colors in RGB
	\definecolor{TUMBlue3}{RGB}{100,160,200}%   Pantone 542
	\definecolor{TUMBlue4}{RGB}{152,198,234}%   Pantone 283
	\definecolor{TUMIvory}{RGB}{218,215,203}%
	\definecolor{TUMOrange}{RGB}{227,114,34}%
	\definecolor{TUMGreen}{RGB}{162,173,0}%
	%
	% Anniversary colors "150 Jahre culture of excellence" (for use in 2018 only)
	\definecolor{TUMAnniMustard}{RGB}{232,200,55}%  Pantone 7405
	\definecolor{TUMAnniMustard2}{RGB}{202,171,41}% Pantone 103
	\definecolor{TUMAnniOrange}{RGB}{247,166,0}%    Pantone 137
	\definecolor{TUMAnniOrange2}{RGB}{243,145,0}%   Pantone 151
	\definecolor{TUMAnniGreen}{RGB}{188,207,30}%    Pantone 382
	\definecolor{TUMAnniGreen2}{RGB}{162,191,22}%   Pantone 376
	\definecolor{TUMAnniBlue}{RGB}{146,212,241}%    Pantone 297
	\definecolor{TUMAnniBlue2}{RGB}{91,197,242}%    Pantone 306
	\definecolor{TUMAnniPink}{RGB}{242,144,149}%    Pantone 708
	\definecolor{TUMAnniPink2}{RGB}{227,130,143}%   Pantone 702
\fi%
%
%
% >>> CONTENTS OF FILE source/FTM/Modules/FTMcolor.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%
%
%===================
%--- Definitions ---
%===================
% FTM logo colors
\ifdefined\optCMYK%
	% FTM logo in cmyk
	\definecolor{FTMLogoColorTop}{cmyk}{36,15,0,15}%    Pantone 300
	\definecolor{FTMLogoColorMiddle}{cmyk}{58,23,0,21}%
	\definecolor{FTMLogoColorBottom}{cmyk}{87,39,0,27}%
\else%
% FTM logo in RGB
	\definecolor{FTMLogoColorTop}{RGB}{140,186,218}%      Pantone 300
	\definecolor{FTMLogoColorMiddle}{RGB}{84,156,202}%
	\definecolor{FTMLogoColorBottom}{RGB}{24,113,185}%
\fi%
%
%
\else\fi% End-check if module FTMcolor is enabled
%###################################################################################################
%--- END MODULE FTMcolor ---------------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- BEGIN MODULE FTMtikz --------------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMtikz% Start-check if module FTMtikz is enabled
%
% >>> CONTENTS OF FILE source/TUM/Modules/TUMtikz.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%================
%--- Packages ---
%================
\RequirePackage{tikz}%
\usetikzlibrary{calc}%
\usetikzlibrary{external}%
\ifdefined\optTikzExternalize%
	\tikzexternalize[prefix=figures/tikzoutput/]%
\else\fi%
\PassOptionsToPackage{framemethod=tikz}{mdframed}%
\RequirePackage{mdframed}%
\RequirePackage{pgfplots}%
\pgfplotsset{compat=newest}%        for Matlab2TikZ
\usetikzlibrary{plotmarks}%         for Matlab2TikZ
\usetikzlibrary{arrows.meta}%       for Matlab2TikZ
\usepgfplotslibrary{patchplots}%    for Matlab2TikZ
\RequirePackage{grffile}%           for Matlab2TikZ
\RequirePackage{pgfgantt}%
%
%
%===================
%--- Definitions ---
%===================
\pgfplotsset{plot coordinates/math parser=false}%   for Matlab2TikZ
\newlength\figureheight%                            for Matlab2TikZ
\newlength\figurewidth%                             for Matlab2TikZ
%
%
%================
%--- Commands ---
%================
% Misc
% ----
\newcommand{\FTMtikzExternalizeSkipNext}{\tikzset{external/export next=false}}%
%
% Grids
% -----
\newcommand{\FTMtikzGrid}[5][line width=1mm]{%
	\FTMtikzExternalizeSkipNext%
	\begin{tikzpicture}[inner sep=0pt, outer sep=0pt]%
		% Horizontal lines:
		\draw[#1] ($ (0mm,0mm) $) -- ($ (#2*#4,0mm) $);%
		\FTMcoreRepetition{#5}{\draw[#1] ($ (0mm,#3*\Step) $) -- ($ (#2*#4,#3*\Step) $);}%
		% Vertical lines:
		\draw[#1] ($ (0mm,0mm) $) -- ($ (0mm,#3*#5) $);%
		\FTMcoreRepetition{#4}{\draw[#1] ($ (#2*\Step,0mm) $) -- ($ (#2*\Step,#3*#5) $);}%
	\end{tikzpicture}%
}%
%
% Frames
% ------
\newcommand{\FTMtikzCircled}[1]{%
	\FTMtikzExternalizeSkipNext%
	\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=1pt] (char) {#1};}%
}%
%
%
% >>> CONTENTS OF FILE source/FTM/Modules/FTMtikz.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%
%
%================
%--- Packages ---
%================
%
% 3D tikz
\RequirePackage{tikz-3dplot}%
\tikzset{font=\footnotesize}
%
%
%
\else\fi% End-check if module FTMtikz is enabled
%###################################################################################################
%--- END MODULE FTMtikz ----------------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- BEGIN MODULE FTMlogo --------------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMlogo% Start-check if module FTMlogo is enabled
%
% >>> CONTENTS OF FILE source/TUM/Modules/TUMlogo.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%================
%--- Commands ---
%================
% Tercets
% -------
\newcommand{\FTMlogoTercetTUM}[2][TUMBlue]{%
	\resizebox*{!}{#2}{%
		\color{#1}%
		\fontsize{8.5}{8.5}\fontfamily{phv}\selectfont%
		\begin{tikzpicture}%
			\node[anchor=south west] at (0cm,0.66cm) {\vphantom{Xg}};%
			\node[anchor=south west] at (0cm,0.33cm) {\vphantom{Xg}};%
			\node[anchor=south west] at (0cm,0cm) {\vphantom{Xg}\FTMlangTUM};%
		\end{tikzpicture}%
	}%
}%
\newcommand{\FTMlogoTercetDepartment}[2][TUMBlue]{%
	\resizebox*{!}{#2}{%
		\color{#1}%
		\fontsize{8.5}{8.5}\fontfamily{phv}\selectfont%
		\begin{tikzpicture}%
			\node[anchor=south west] at (0cm,0.66cm) {\vphantom{Xg}};%
			\node[anchor=south west] at (0cm,0.33cm) {\vphantom{Xg}\FTMlangDepartment};%
			\node[anchor=south west] at (0cm,0cm) {\vphantom{Xg}\FTMlangTUM};%
		\end{tikzpicture}%
	}%
}%
\newcommand{\FTMlogoTercetChair}[2][TUMBlue]{%
	\resizebox*{!}{#2}{%
		\color{#1}%
		\fontsize{8.5}{8.5}\fontfamily{phv}\selectfont%
		\begin{tikzpicture}%
			\node[anchor=south west] at (0cm,0.66cm) {\vphantom{Xg}\FTMlangChair};%
			\node[anchor=south west] at (0cm,0.33cm) {\vphantom{Xg}\FTMlangDepartment};%
			\node[anchor=south west] at (0cm,0cm) {\vphantom{Xg}\FTMlangTUM};%
		\end{tikzpicture}%
	}%
}%
%
% Logos
% -----
\newcommand{\FTMlogoTUM}[3][!]{%
	\resizebox{#1}{#2}{%
		\FTMtikzExternalizeSkipNext%
		\begin{tikzpicture}[y=0.80pt, x=0.80pt, yscale=-1, xscale=1, inner sep=0pt, outer sep=0pt]%
		\begin{scope}[even odd rule,line width=0.800pt]%
		\begin{scope}[fill=#3]%
			\path[fill] (405,0) -- (370,0) -- (370,320) -- (290,320) -- (290,0) -- (255,0) -- (0,0) --
				(0,70) -- (70,70) -- (70,390) -- (140,390) -- (140,70) -- (220,70) -- (220,390) --
				(255,390) -- (405,390) -- (440,390) -- (440,70) -- (520,70) -- (520,390) -- (590,390) --
				(590,70) --  (670,70) -- (670,390) -- (740,390) -- (740,35) -- (740,0) -- (405,0) -- cycle;
		\end{scope}%
		\end{scope}%
		\end{tikzpicture}%
	}%
}%
\newcommand{\FTMlogoDepartment}[3][!]{%
	\resizebox{#1}{#2}{%
		\FTMtikzExternalizeSkipNext%
		\begin{tikzpicture}[y=0.80pt, x=0.80pt, yscale=-1, xscale=1, inner sep=0pt, outer sep=0pt]%
			\begin{scope}[even odd rule,line width=0.800pt]%
				\begin{scope}[shift={(-3366.0,-39.0)},fill=#3]%
					\path[fill] (3848.2448,185.1588) .. controls (3842.0586,169.7349) and
						(3827.6725,147.4471) .. (3816.1689,135.4551) .. controls (3814.8263,134.0613)
						and (3783.0794,101.2148) .. (3746.9364,86.3300) -- (3743.6459,94.2852) ..
						controls (3778.0910,108.4731) and (3809.6141,141.0829) .. (3809.9432,141.4117)
						.. controls (3820.8019,152.7330) and (3834.3983,173.7980) ..
						(3840.2291,188.3672) -- (3867.1192,255.3883) -- (3875.1217,252.1799) --
						(3848.2448,185.1588) -- (3848.2448,185.1588) -- cycle(3475.7058,358.7799) ..
						controls (3477.0352,360.1737) and (3508.8084,393.0071) .. (3544.9251,407.8787)
						-- (3548.2024,399.9104) .. controls (3513.7705,385.7487) and
						(3482.2342,353.1521) .. (3481.9314,352.8365) .. controls (3471.0596,341.4888)
						and (3457.4763,320.4370) .. (3451.6324,305.8809) -- (3424.7291,238.8204) --
						(3416.7266,242.0288) -- (3443.6298,309.0762) .. controls (3449.8160,324.5001)
						and (3464.2022,346.7879) .. (3475.7058,358.7799) -- (3475.7058,358.7799) --
						cycle(3464.7813,238.7152) .. controls (3462.5042,221.2663) and
						(3462.4911,203.5413) .. (3464.7813,186.0266) .. controls (3467.2952,166.7895)
						and (3470.4410,157.8612) .. (3470.4541,157.7692) .. controls
						(3475.8111,142.9369) and (3488.0913,120.7938) .. (3497.8444,108.3942) --
						(3542.7270,51.3796) -- (3535.9617,46.0673) -- (3491.0659,103.0819) .. controls
						(3480.8522,116.0733) and (3467.9665,139.3078) .. (3462.3595,154.8501) ..
						controls (3462.2147,155.2445) and (3458.8847,164.5936) .. (3456.2391,184.9090)
						.. controls (3453.8568,203.1731) and (3453.8568,221.6476) ..
						(3456.2523,239.8329) -- (3464.7813,238.7152) -- (3464.7813,238.7152) --
						cycle(3636.4277,52.5498) .. controls (3651.3798,48.7366) and
						(3676.9011,47.3691) .. (3692.1559,49.5650) -- (3764.0339,59.8476) --
						(3765.2448,51.3270) -- (3693.3931,41.0312) .. controls (3676.9274,38.6907) and
						(3650.4190,40.1108) .. (3634.2823,44.2001) .. controls (3632.3870,44.6998) and
						(3587.4122,56.3236) .. (3557.4422,79.3346) -- (3562.6939,86.1590) .. controls
						(3591.2292,64.2394) and (3635.9802,52.6682) .. (3636.4277,52.5498) --
						(3636.4277,52.5498) -- cycle(3644.9173,441.2907) -- (3366.0000,441.2907) --
						(3366.0000,449.9033) -- (3645.9965,449.9033) -- (3645.9965,449.8376) ..
						controls (3753.8728,449.2459) and (3841.4795,361.4360) .. (3841.4795,253.5080)
						-- (3832.8583,253.5080) .. controls (3832.8583,357.0442) and
						(3748.5422,441.2907) .. (3644.9173,441.2907) -- (3644.9173,441.2907) -- cycle;
				\end{scope}%
			\end{scope}%
		\end{tikzpicture}%
	}%
}%
%
% Badges
% ------
\newcommand{\FTMlogoAnniversary}[2][1cm]{%
	\resizebox{!}{2.654928#1}{%
		\FTMtikzExternalizeSkipNext%
		\begin{tikzpicture}[y=0.80pt, x=0.80pt, yscale=-1, xscale=1, inner sep=0pt, outer sep=0pt]%
			\begin{scope}[shift={(0,-0.00391)}]%
				\path[fill=#2,nonzero rule] (0.0000,0.0039) -- (12.4844,75.2617) --
					(118.8750,56.6875) -- (118.8750,0.0039) -- (0.0000,0.0039);
				\path[fill=TUMWhite,nonzero rule] (22.6523,28.5781) .. controls (22.6133,28.5586)
					and (22.2930,28.3984) .. (22.2539,28.3789) .. controls (21.6797,28.0938) and
					(21.0977,27.9492) .. (20.5156,27.9492) .. controls (19.8047,27.9492) and
					(19.1758,28.0938) .. (18.6484,28.3750) .. controls (18.1211,28.6523) and
					(17.7266,29.0352) .. (17.4375,29.5430) .. controls (17.1523,30.0430) and
					(17.0039,30.6172) .. (17.0039,31.3086) .. controls (17.0039,32.0000) and
					(17.1523,32.5859) .. (17.4375,33.0898) .. controls (17.7266,33.5938) and
					(18.1211,33.9766) .. (18.6484,34.2578) .. controls (19.1797,34.5391) and
					(19.8047,34.6797) .. (20.5156,34.6797) .. controls (21.1406,34.6797) and
					(21.7617,34.5156) .. (22.3750,34.1914) .. controls (22.3750,34.1914) and
					(22.4297,34.1641) .. (22.4531,34.1445) .. controls (22.5039,34.1016) and
					(22.5156,34.0391) .. (22.4844,33.9492) -- (22.1094,33.1836) .. controls
					(22.0508,33.0781) and (21.9648,33.0391) .. (21.8555,33.0742) .. controls
					(21.8555,33.0742) and (21.6563,33.1602) .. (21.5547,33.1914) .. controls
					(20.8906,33.4063) and (20.0352,33.3203) .. (19.5469,33.0703) .. controls
					(19.2461,32.9141) and (19.0039,32.6367) .. (18.8203,32.3438) .. controls
					(18.6406,32.0508) and (18.5469,31.7031) .. (18.5469,31.3164) .. controls
					(18.5469,30.9258) and (18.6406,30.5820) .. (18.8203,30.2891) .. controls
					(19.0039,29.9961) and (19.2461,29.7148) .. (19.5469,29.5625) .. controls
					(20.0352,29.3125) and (20.9414,29.2227) .. (21.6055,29.4375) .. controls
					(21.6563,29.4570) and (21.7344,29.4844) .. (21.7969,29.5117) .. controls
					(21.8594,29.5352) and (22.1563,29.6875) .. (22.1563,29.6875) .. controls
					(22.2656,29.7227) and (22.3477,29.6836) .. (22.4063,29.5781) --
					(22.7656,28.8242) .. controls (22.7969,28.7344) and (22.7852,28.6719) ..
					(22.7305,28.6250) .. controls (22.7109,28.6094) and (22.6523,28.5781) ..
					(22.6523,28.5781);
				\path[fill=TUMWhite,nonzero rule] (28.9766,28.1328) -- (27.6992,28.1328) ..
					controls (27.5938,28.1328) and (27.5313,28.1758) .. (27.5117,28.2656) --
					(27.5117,32.5078) -- (27.4023,32.6641) .. controls (27.1211,32.9609) and
					(26.7305,33.1055) .. (26.4609,33.1094) .. controls (26.2305,33.1133) and
					(26.1133,33.0937) .. (25.9648,33.0234) .. controls (25.5625,32.8438) and
					(25.3789,32.5195) .. (25.3789,32.0430) -- (25.3789,28.2188) .. controls
					(25.3633,28.1641) and (25.3086,28.1328) .. (25.2188,28.1328) --
					(23.9453,28.1328) .. controls (23.8125,28.1328) and (23.7461,28.1992) ..
					(23.7461,28.3281) -- (23.7461,32.2266) .. controls (23.7461,32.7500) and
					(23.8398,33.2031) .. (24.0273,33.5742) .. controls (24.2031,33.9297) and
					(24.4570,34.1992) .. (24.7969,34.3867) .. controls (25.1445,34.5820) and
					(25.6406,34.6797) .. (25.8672,34.6797) .. controls (26.9414,34.6797) and
					(27.2578,34.1992) .. (27.6836,33.6836) .. controls (27.6836,33.6836) and
					(27.9141,34.3516) .. (27.9297,34.3750) .. controls (27.9766,34.4492) and
					(28.0313,34.4844) .. (28.0938,34.4844) -- (28.9453,34.4844) .. controls
					(28.9961,34.4844) and (29.0391,34.4648) .. (29.0781,34.4258) .. controls
					(29.1133,34.3867) and (29.1367,34.3477) .. (29.1367,34.3047) .. controls
					(29.1367,34.3047) and (29.1406,28.2891) .. (29.1406,28.2617) .. controls
					(29.1406,28.1758) and (29.0859,28.1328) .. (28.9766,28.1328);
				\path[fill=TUMWhite,nonzero rule] (33.6758,20.3789) .. controls (33.6758,20.5039)
					and (33.7344,20.5664) .. (33.8594,20.5664) -- (36.0156,20.5664) .. controls
					(36.1328,20.5664) and (36.1914,20.5039) .. (36.1914,20.3789) --
					(36.1914,12.1680) .. controls (36.1914,12.0625) and (36.1328,12.0234) ..
					(36.0156,12.0430) -- (32.8711,12.5313) .. controls (32.7383,12.5469) and
					(32.6719,12.6094) .. (32.6719,12.7148) -- (32.6719,14.2188) .. controls
					(32.6562,14.3164) and (32.7109,14.3672) .. (32.8359,14.3672) --
					(33.6758,14.3672) -- (33.6758,20.3789);
				\path[fill=TUMWhite,nonzero rule] (32.0430,25.8594) -- (30.7656,25.8594) ..
					controls (30.6562,25.8594) and (30.5938,25.9062) .. (30.5742,25.9922) --
					(30.5742,34.3555) .. controls (30.5742,34.4414) and (30.6289,34.4844) ..
					(30.7383,34.4844) -- (32.0156,34.4844) .. controls (32.1250,34.4844) and
					(32.1875,34.4414) .. (32.2070,34.3516) -- (32.2070,25.9883) .. controls
					(32.2070,25.9023) and (32.1523,25.8594) .. (32.0430,25.8594);
				\path[fill=TUMWhite,nonzero rule] (65.4648,26.9688) .. controls (65.3008,27.2969)
					and (65.2109,27.6875) .. (65.1914,28.1328) -- (64.3945,28.1328) .. controls
					(64.3047,28.1289) and (64.2617,28.1719) .. (64.2617,28.2695) --
					(64.2617,28.9883) .. controls (64.2617,29.0234) and (64.2773,29.0547) ..
					(64.3047,29.0820) .. controls (64.3359,29.1055) and (64.3633,29.1172) ..
					(64.3945,29.1172) -- (65.1836,29.1172) -- (65.1875,34.3438) .. controls
					(65.1875,34.3828) and (65.1992,34.4180) .. (65.2305,34.4453) .. controls
					(65.2578,34.4688) and (65.2891,34.4844) .. (65.3242,34.4844) --
					(66.6797,34.4844) .. controls (66.7148,34.4844) and (66.7461,34.4687) ..
					(66.7773,34.4414) .. controls (66.8047,34.4141) and (66.8203,34.3789) ..
					(66.8203,34.3437) -- (66.8203,29.1172) -- (67.7187,29.1172) .. controls
					(67.8008,29.1172) and (67.8477,29.0703) .. (67.8594,28.9805) --
					(67.9570,28.2578) .. controls (67.9570,28.1758) and (67.9102,28.1328) ..
					(67.8203,28.1328) -- (66.8203,28.1328) .. controls (66.8242,27.6953) and
					(66.9023,27.4297) .. (67.0977,27.2266) .. controls (67.3008,27.0156) and
					(67.4922,26.9453) .. (67.8438,26.9453) -- (67.8711,26.9453) .. controls
					(67.9102,26.9453) and (67.9414,26.9336) .. (67.9688,26.9023) .. controls
					(67.9961,26.8750) and (68.0117,26.8437) .. (68.0117,26.8086) --
					(68.0117,26.0000) .. controls (68.0117,25.9648) and (67.9961,25.9297) ..
					(67.9688,25.9023) .. controls (67.9375,25.8750) and (67.9063,25.8594) ..
					(67.8711,25.8594) -- (67.5391,25.8594) -- (67.5391,25.8633) .. controls
					(67.5273,25.8633) and (67.5195,25.8594) .. (67.5078,25.8594) .. controls
					(67.0117,25.8594) and (66.5859,25.9609) .. (66.2383,26.1523) .. controls
					(65.8984,26.3437) and (65.6445,26.6133) .. (65.4648,26.9687);
				\path[fill=TUMWhite,nonzero rule] (47.1328,28.0234) .. controls (46.4883,28.1797)
					and (46.2695,28.3555) .. (45.9453,28.7500) .. controls (45.9453,28.7500) and
					(45.7773,28.2656) .. (45.7617,28.2422) .. controls (45.7148,28.1680) and
					(45.6562,28.1328) .. (45.5938,28.1328) -- (44.8477,28.1328) .. controls
					(44.7969,28.1328) and (44.7539,28.1523) .. (44.7148,28.1914) .. controls
					(44.6758,28.2266) and (44.6563,28.2695) .. (44.6563,28.3086) .. controls
					(44.6563,28.3086) and (44.6485,34.3281) .. (44.6485,34.3555) .. controls
					(44.6485,34.4414) and (44.7031,34.4844) .. (44.8125,34.4844) --
					(46.0938,34.4844) .. controls (46.1992,34.4844) and (46.2617,34.4414) ..
					(46.2813,34.3516) -- (46.2813,29.7031) .. controls (46.4219,29.4336) and
					(46.7891,29.2578) .. (47.1836,29.2578) -- (47.7149,29.2578) .. controls
					(47.7969,29.2578) and (47.8399,29.2070) .. (47.8399,29.0977) --
					(47.8399,28.1797) .. controls (47.8399,28.1016) and (47.8164,28.0469) ..
					(47.7695,28.0156) .. controls (47.7539,28.0039) and (47.7344,27.9961) ..
					(47.7110,27.9922) .. controls (47.4961,27.9961) and (47.3203,27.9766) ..
					(47.1328,28.0234);
				\path[fill=TUMWhite,nonzero rule] (63.3555,18.1797) .. controls (63.4492,18.1016)
					and (63.5938,18.0625) .. (63.7891,18.0625) .. controls (63.9883,18.0625) and
					(64.1914,18.1641) .. (64.3945,18.3672) -- (64.3945,18.6328) .. controls
					(64.1914,18.8359) and (63.9844,18.9375) .. (63.7734,18.9375) .. controls
					(63.5859,18.9375) and (63.4453,18.8984) .. (63.3516,18.8203) .. controls
					(63.2578,18.7461) and (63.2148,18.6367) .. (63.2148,18.5039) .. controls
					(63.2148,18.3672) and (63.2617,18.2617) .. (63.3555,18.1797) --
					cycle(61.5938,20.4766) .. controls (61.9453,20.6602) and (62.3477,20.7500) ..
					(62.8086,20.7500) .. controls (63.7656,20.7500) and (64.4648,20.5156) ..
					(64.9062,20.0508) -- (64.9961,20.3789) .. controls (64.9961,20.4297) and
					(65.0156,20.4687) .. (65.0547,20.5078) .. controls (65.0937,20.5469) and
					(65.1367,20.5664) .. (65.1836,20.5664) -- (66.7226,20.5664) .. controls
					(66.7734,20.5664) and (66.8164,20.5469) .. (66.8555,20.5078) .. controls
					(66.8906,20.4688) and (66.9062,20.4297) .. (66.9062,20.3789) --
					(66.9062,17.2227) .. controls (66.9062,16.0117) and (66.6601,15.1172) ..
					(66.1601,14.5430) .. controls (65.6601,13.9687) and (64.8867,13.6836) ..
					(63.8398,13.6836) .. controls (62.7930,13.6836) and (61.9062,13.9141) ..
					(61.1758,14.3789) .. controls (61.1172,14.4219) and (61.0898,14.4727) ..
					(61.0898,14.5273) .. controls (61.0898,14.5508) and (61.0976,14.5781) ..
					(61.1094,14.6133) -- (61.8047,16.0703) .. controls (61.8398,16.1367) and
					(61.8828,16.1680) .. (61.9453,16.1680) .. controls (61.9687,16.1680) and
					(62.0000,16.1563) .. (62.0312,16.1367) .. controls (62.2539,16.0117) and
					(62.4805,15.9180) .. (62.7109,15.8633) .. controls (62.9414,15.8086) and
					(63.1914,15.7813) .. (63.4570,15.7813) .. controls (63.7383,15.7813) and
					(63.9648,15.8594) .. (64.1367,16.0156) .. controls (64.3047,16.1758) and
					(64.3945,16.3867) .. (64.3945,16.6484) -- (64.3945,17.1641) .. controls
					(64.2734,16.9648) and (64.0703,16.8047) .. (63.7812,16.6875) .. controls
					(63.4922,16.5703) and (63.1680,16.5117) .. (62.8086,16.5117) .. controls
					(62.3438,16.5117) and (61.9336,16.5977) .. (61.5859,16.7656) .. controls
					(61.2344,16.9336) and (60.9648,17.1758) .. (60.7734,17.4922) .. controls
					(60.5859,17.8047) and (60.4883,18.1719) .. (60.4883,18.5977) .. controls
					(60.4883,19.0117) and (60.5859,19.3828) .. (60.7773,19.7109) .. controls
					(60.9688,20.0391) and (61.2422,20.2930) .. (61.5938,20.4766);
				\path[fill=TUMWhite,nonzero rule] (36.6680,28.1328) -- (35.6680,28.1328) --
					(35.6680,26.4688) .. controls (35.6680,26.4297) and (35.6562,26.3984) ..
					(35.6250,26.3711) .. controls (35.5977,26.3438) and (35.5664,26.3320) ..
					(35.5312,26.3398) -- (34.1758,26.4687) .. controls (34.0820,26.4765) and
					(34.0352,26.5195) .. (34.0352,26.5937) -- (34.0352,28.1328) --
					(33.2422,28.1328) .. controls (33.1562,28.1289) and (33.1133,28.1719) ..
					(33.1133,28.2695) -- (33.1133,28.9609) .. controls (33.1133,28.9961) and
					(33.1289,29.0273) .. (33.1562,29.0547) .. controls (33.1836,29.0781) and
					(33.2148,29.0937) .. (33.2422,29.0937) -- (34.0352,29.0937) --
					(34.0352,34.3437) .. controls (34.0352,34.3828) and (34.0508,34.4180) ..
					(34.0781,34.4453) .. controls (34.1094,34.4687) and (34.1406,34.4844) ..
					(34.1758,34.4844) -- (35.5313,34.4844) .. controls (35.5664,34.4844) and
					(35.5977,34.4687) .. (35.6250,34.4414) .. controls (35.6563,34.4141) and
					(35.6680,34.3789) .. (35.6680,34.3437) -- (35.6680,29.0937) --
					(36.5703,29.0937) .. controls (36.6484,29.0937) and (36.6953,29.0469) ..
					(36.7109,28.9531) -- (36.8047,28.2578) .. controls (36.8047,28.1758) and
					(36.7617,28.1328) .. (36.6680,28.1328);
				\path[fill=TUMWhite,nonzero rule] (62.2109,32.2930) .. controls (62.0469,32.6016)
					and (61.8164,32.8438) .. (61.5234,33.0156) .. controls (61.2266,33.1875) and
					(60.8945,33.2734) .. (60.5273,33.2734) .. controls (60.1602,33.2734) and
					(59.8281,33.1875) .. (59.5352,33.0195) .. controls (59.2383,32.8516) and
					(59.0078,32.6133) .. (58.8438,32.3047) .. controls (58.6914,32.0117) and
					(58.6133,31.6797) .. (58.6133,31.3125) .. controls (58.6133,30.9453) and
					(58.6914,30.6133) .. (58.8438,30.3203) .. controls (59.0078,30.0117) and
					(59.2383,29.7734) .. (59.5352,29.6016) .. controls (59.8281,29.4336) and
					(60.1602,29.3516) .. (60.5273,29.3516) .. controls (61.0859,29.3516) and
					(61.5547,29.5352) .. (61.9141,29.9023) .. controls (62.2656,30.2695) and
					(62.4375,30.7383) .. (62.4375,31.2969) .. controls (62.4375,31.6641) and
					(62.3594,32.0000) .. (62.2109,32.2930) -- cycle(62.3359,28.3672) .. controls
					(61.8164,28.0859) and (61.2109,27.9453) .. (60.5273,27.9453) .. controls
					(59.8477,27.9453) and (59.2422,28.0859) .. (58.7266,28.3672) .. controls
					(58.2109,28.6445) and (57.8203,29.0273) .. (57.5312,29.5352) .. controls
					(57.2461,30.0430) and (57.1016,30.6406) .. (57.1016,31.3203) .. controls
					(57.1016,31.9922) and (57.2461,32.5859) .. (57.5312,33.0898) .. controls
					(57.8164,33.5977) and (58.2031,33.9805) .. (58.7188,34.2578) .. controls
					(59.2344,34.5391) and (59.8438,34.6797) .. (60.5273,34.6797) .. controls
					(61.2109,34.6797) and (61.8164,34.5391) .. (62.3320,34.2539) .. controls
					(62.8477,33.9727) and (63.2383,33.5898) .. (63.5234,33.0820) .. controls
					(63.8047,32.5781) and (63.9531,31.9766) .. (63.9531,31.3047) .. controls
					(63.9531,30.6328) and (63.8086,30.0391) .. (63.5234,29.5352) .. controls
					(63.2383,29.0273) and (62.8477,28.6445) .. (62.3359,28.3672);
				\path[fill=TUMWhite,nonzero rule] (47.3750,15.2031) .. controls (47.4883,14.8711)
					and (47.6484,14.6172) .. (47.8555,14.4336) .. controls (48.0625,14.2500) and
					(48.3008,14.1602) .. (48.5781,14.1602) .. controls (48.8477,14.1602) and
					(49.0859,14.2500) .. (49.2930,14.4297) .. controls (49.5039,14.6094) and
					(49.6641,14.8633) .. (49.7812,15.1914) .. controls (49.8945,15.5195) and
					(49.9531,15.8984) .. (49.9531,16.3281) .. controls (49.9531,16.7656) and
					(49.8945,17.1523) .. (49.7812,17.4883) .. controls (49.6641,17.8242) and
					(49.5039,18.0820) .. (49.2930,18.2695) .. controls (49.0859,18.4570) and
					(48.8477,18.5508) .. (48.5781,18.5508) .. controls (48.3125,18.5508) and
					(48.0742,18.4570) .. (47.8633,18.2734) .. controls (47.6562,18.0898) and
					(47.4961,17.8320) .. (47.3789,17.5000) .. controls (47.2656,17.1680) and
					(47.2070,16.7852) .. (47.2070,16.3516) .. controls (47.2070,15.9141) and
					(47.2617,15.5313) .. (47.3750,15.2031) -- cycle(46.5078,20.2031) .. controls
					(47.1094,20.5664) and (47.8008,20.7500) .. (48.5898,20.7500) .. controls
					(49.3750,20.7500) and (50.0664,20.5664) .. (50.6641,20.2031) .. controls
					(51.2578,19.8359) and (51.7188,19.3203) .. (52.0469,18.6562) .. controls
					(52.3750,17.9883) and (52.5391,17.2227) .. (52.5391,16.3516) .. controls
					(52.5391,15.4766) and (52.3750,14.7109) .. (52.0430,14.0469) .. controls
					(51.7148,13.3828) and (51.2539,12.8672) .. (50.6562,12.5039) .. controls
					(50.0625,12.1406) and (49.3711,11.9609) .. (48.5820,11.9609) .. controls
					(47.7969,11.9609) and (47.1055,12.1406) .. (46.5078,12.5039) .. controls
					(45.9062,12.8672) and (45.4453,13.3828) .. (45.1133,14.0469) .. controls
					(44.7852,14.7109) and (44.6211,15.4766) .. (44.6211,16.3516) .. controls
					(44.6211,17.2227) and (44.7852,17.9883) .. (45.1133,18.6562) .. controls
					(45.4453,19.3203) and (45.9102,19.8359) .. (46.5078,20.2031);
				\path[fill=TUMWhite,nonzero rule] (52.7812,30.8242) -- (49.9219,30.8242) ..
					controls (49.9219,30.0156) and (50.5898,29.5039) .. (51.4297,29.5039) ..
					controls (52.2656,29.5039) and (52.7812,30.0156) .. (52.7812,30.8242) --
					cycle(48.6289,29.5547) .. controls (48.3203,30.0586) and (48.1680,30.7344) ..
					(48.1680,31.3164) .. controls (48.1680,31.8984) and (48.3125,32.6094) ..
					(48.6406,33.0977) .. controls (49.2891,34.0703) and (50.2773,34.6758) ..
					(51.5430,34.6797) .. controls (52.4258,34.6836) and (53.5547,34.1328) ..
					(53.5508,34.1289) -- (53.5547,34.1328) .. controls (53.6680,34.0820) and
					(53.7070,33.9961) .. (53.6719,33.8750) -- (53.3398,33.0234) .. controls
					(53.2812,32.9062) and (53.1875,32.8750) .. (53.0703,32.9297) .. controls
					(53.0703,32.9297) and (53.0664,32.9297) .. (53.0625,32.9297) .. controls
					(52.4102,33.1289) and (52.2461,33.2695) .. (51.5234,33.2695) .. controls
					(50.6367,33.2695) and (49.9219,32.6406) .. (49.9219,31.9258) --
					(53.9024,31.9258) .. controls (54.0195,31.9102) and (54.0742,31.8828) ..
					(54.1094,31.7188) .. controls (54.1719,31.4180) and (54.1680,31.0703) ..
					(54.1680,30.8750) .. controls (54.1680,30.1953) and (54.0078,29.6953) ..
					(53.7422,29.2500) .. controls (53.1250,28.2227) and (51.9922,27.9609) ..
					(51.4492,27.9609) .. controls (50.9063,27.9609) and (49.5039,28.1211) ..
					(48.6289,29.5547);
				\path[fill=TUMWhite,nonzero rule] (56.4414,41.9805) .. controls (56.4727,41.8867)
					and (56.4141,41.8203) .. (56.3398,41.8203) -- (54.5586,41.8203) .. controls
					(54.4727,41.8203) and (54.3984,41.8711) .. (54.3516,41.9688) --
					(53.4453,43.9609) -- (52.5352,41.9688) .. controls (52.4922,41.8711) and
					(52.4141,41.8203) .. (52.3281,41.8203) -- (50.5469,41.8203) .. controls
					(50.4727,41.8203) and (50.4141,41.8867) .. (50.4453,41.9805) --
					(52.3789,45.0195) -- (50.3867,48.1484) .. controls (50.3359,48.2461) and
					(50.4062,48.3164) .. (50.4961,48.3164) -- (52.2656,48.3164) .. controls
					(52.3867,48.3164) and (52.4570,48.2617) .. (52.4805,48.1602) --
					(53.4375,45.9727) -- (54.4102,48.1602) .. controls (54.4297,48.2617) and
					(54.5000,48.3164) .. (54.6211,48.3164) -- (56.3906,48.3164) .. controls
					(56.4844,48.3164) and (56.5508,48.2461) .. (56.5000,48.1484) --
					(54.5078,45.0195) -- (56.4414,41.9805);
				\path[fill=TUMWhite,nonzero rule] (83.0273,15.8828) .. controls (83.1914,15.7227)
					and (83.4102,15.6406) .. (83.6758,15.6406) .. controls (83.9336,15.6406) and
					(84.1367,15.7227) .. (84.2891,15.8828) .. controls (84.4375,16.0430) and
					(84.5156,16.2617) .. (84.5156,16.5312) -- (82.7812,16.5312) .. controls
					(82.7812,16.2617) and (82.8633,16.0430) .. (83.0273,15.8828) --
					cycle(86.3086,20.0625) .. controls (86.3867,20.0078) and (86.4141,19.9492) ..
					(86.3906,19.8789) -- (85.8672,18.3672) .. controls (85.8437,18.2891) and
					(85.8086,18.2539) .. (85.7617,18.2539) .. controls (85.7383,18.2539) and
					(85.7148,18.2578) .. (85.6875,18.2695) .. controls (85.1055,18.5430) and
					(84.4805,18.6758) .. (83.8164,18.6758) .. controls (83.5117,18.6758) and
					(83.2656,18.5938) .. (83.0742,18.4297) .. controls (82.8867,18.2617) and
					(82.7930,18.0469) .. (82.7930,17.7813) -- (86.5937,17.7813) .. controls
					(86.7109,17.7813) and (86.7734,17.7266) .. (86.7852,17.6172) .. controls
					(86.8125,17.3672) and (86.8281,17.1211) .. (86.8281,16.8711) .. controls
					(86.8281,16.1641) and (86.6953,15.5703) .. (86.4336,15.0938) .. controls
					(86.1719,14.6172) and (85.8047,14.2617) .. (85.3359,14.0313) .. controls
					(84.8633,13.7969) and (84.3164,13.6836) .. (83.6914,13.6836) .. controls
					(83.0078,13.6836) and (82.4023,13.8281) .. (81.8672,14.1250) .. controls
					(81.3359,14.4219) and (80.9219,14.8359) .. (80.6289,15.3750) .. controls
					(80.3320,15.9102) and (80.1836,16.5273) .. (80.1836,17.2227) .. controls
					(80.1836,17.9180) and (80.3320,18.5313) .. (80.6328,19.0664) .. controls
					(80.9297,19.6016) and (81.3477,20.0156) .. (81.8828,20.3086) .. controls
					(82.4180,20.6016) and (83.0273,20.7500) .. (83.7187,20.7500) .. controls
					(84.7578,20.7500) and (85.6211,20.5195) .. (86.3086,20.0625);
				\path[fill=TUMWhite,nonzero rule] (77.5898,44.6562) .. controls (77.5898,43.8477)
					and (78.2578,43.3359) .. (79.1016,43.3359) .. controls (79.9336,43.3359) and
					(80.4531,43.8477) .. (80.4531,44.6562) -- cycle(79.1172,41.7930) .. controls
					(78.5742,41.7930) and (77.1719,41.9531) .. (76.2969,43.3867) .. controls
					(75.9922,43.8906) and (75.8398,44.5703) .. (75.8398,45.1484) .. controls
					(75.8398,45.7305) and (75.9805,46.4414) .. (76.3086,46.9297) .. controls
					(76.9609,47.9023) and (77.9453,48.5078) .. (79.2109,48.5117) .. controls
					(80.0977,48.5156) and (81.2227,47.9648) .. (81.2227,47.9609) --
					(81.2227,47.9648) .. controls (81.3359,47.9141) and (81.3750,47.8281) ..
					(81.3398,47.7070) -- (81.0117,46.8555) .. controls (80.9492,46.7383) and
					(80.8594,46.7070) .. (80.7383,46.7617) .. controls (80.7383,46.7617) and
					(80.7383,46.7617) .. (80.7305,46.7617) .. controls (80.0781,46.9609) and
					(79.9180,47.1016) .. (79.1914,47.1016) .. controls (78.3047,47.1016) and
					(77.5899,46.4727) .. (77.5899,45.7578) -- (81.5703,45.7578) .. controls
					(81.6875,45.7422) and (81.7422,45.7148) .. (81.7774,45.5508) .. controls
					(81.8438,45.2500) and (81.8399,44.8984) .. (81.8399,44.7070) .. controls
					(81.8399,44.0273) and (81.6758,43.5273) .. (81.4102,43.0820) .. controls
					(80.7930,42.0547) and (79.6602,41.7930) .. (79.1172,41.7930);
				\path[fill=TUMWhite,nonzero rule] (74.5469,39.6914) -- (73.2734,39.6914) ..
					controls (73.1641,39.6914) and (73.1016,39.7383) .. (73.0820,39.8242) --
					(73.0820,48.1875) .. controls (73.0820,48.2734) and (73.1367,48.3164) ..
					(73.2461,48.3164) -- (74.5234,48.3164) .. controls (74.6328,48.3164) and
					(74.6953,48.2734) .. (74.7148,48.1836) -- (74.7148,39.8203) .. controls
					(74.7148,39.7344) and (74.6602,39.6914) .. (74.5469,39.6914);
				\path[fill=TUMWhite,nonzero rule] (75.9805,20.5664) -- (78.1328,20.5664) ..
					controls (78.1797,20.5664) and (78.2227,20.5469) .. (78.2617,20.5078) ..
					controls (78.2969,20.4688) and (78.3164,20.4297) .. (78.3164,20.3789) --
					(78.3164,16.2930) .. controls (78.3984,16.1367) and (78.5313,16.0117) ..
					(78.7266,15.9180) .. controls (78.9180,15.8281) and (79.1289,15.7813) ..
					(79.3555,15.7813) -- (79.6719,15.7813) .. controls (79.7852,15.7891) and
					(79.8438,15.7305) .. (79.8438,15.6133) -- (79.8438,14.0195) .. controls
					(79.8438,13.9102) and (79.7852,13.8555) .. (79.6719,13.8555) --
					(79.3555,13.8555) .. controls (78.6797,13.8555) and (78.1406,14.0977) ..
					(77.7383,14.5820) -- (77.5586,14.0352) .. controls (77.5078,13.9141) and
					(77.4453,13.8555) .. (77.3633,13.8555) -- (75.9805,13.8555) .. controls
					(75.9336,13.8555) and (75.8906,13.8711) .. (75.8555,13.9102) .. controls
					(75.8203,13.9453) and (75.8008,13.9805) .. (75.8008,14.0195) --
					(75.8008,20.3789) .. controls (75.8008,20.4336) and (75.8203,20.4766) ..
					(75.8555,20.5117) .. controls (75.8906,20.5469) and (75.9336,20.5664) ..
					(75.9805,20.5664);
				\path[fill=TUMWhite,nonzero rule] (97.2656,44.6562) .. controls (97.2656,43.8477)
					and (97.9297,43.3359) .. (98.7734,43.3359) .. controls (99.6094,43.3359) and
					(100.1250,43.8477) .. (100.1250,44.6562) -- cycle(101.0859,43.0820) ..
					controls (100.4648,42.0547) and (99.3359,41.7930) .. (98.7930,41.7930) ..
					controls (98.2500,41.7930) and (96.8477,41.9531) .. (95.9688,43.3867) ..
					controls (95.6641,43.8906) and (95.5117,44.5703) .. (95.5117,45.1484) ..
					controls (95.5117,45.7305) and (95.6562,46.4414) .. (95.9805,46.9297) ..
					controls (96.6328,47.9023) and (97.6211,48.5078) .. (98.8867,48.5117) ..
					controls (99.7695,48.5156) and (100.8945,47.9648) .. (100.8945,47.9609) --
					(100.8945,47.9648) .. controls (101.0117,47.9141) and (101.0508,47.8281) ..
					(101.0117,47.7070) -- (100.6836,46.8555) .. controls (100.6211,46.7383) and
					(100.5312,46.7070) .. (100.4141,46.7617) .. controls (100.4141,46.7617) and
					(100.4101,46.7617) .. (100.4061,46.7617) .. controls (99.7537,46.9609) and
					(99.5897,47.1016) .. (98.8670,47.1016) .. controls (97.9764,47.1016) and
					(97.2654,46.4727) .. (97.2654,45.7578) -- (101.2420,45.7578) .. controls
					(101.3592,45.7422) and (101.4139,45.7148) .. (101.4490,45.5508) .. controls
					(101.5154,45.2500) and (101.5115,44.8984) .. (101.5115,44.7070) .. controls
					(101.5115,44.0273) and (101.3514,43.5273) .. (101.0857,43.0820);
				\path[fill=TUMWhite,nonzero rule] (87.2539,42.0625) .. controls (86.9062,41.8672)
					and (86.4102,41.7695) .. (86.1836,41.7695) .. controls (85.1094,41.7695) and
					(84.7930,42.2500) .. (84.3672,42.7656) .. controls (84.3672,42.7656) and
					(84.1367,42.0977) .. (84.1211,42.0742) .. controls (84.0742,42.0000) and
					(84.0195,41.9648) .. (83.9570,41.9648) -- (83.0820,41.9648) .. controls
					(83.0313,41.9648) and (82.9883,41.9844) .. (82.9492,42.0234) .. controls
					(82.9102,42.0586) and (82.8906,42.1016) .. (82.8906,42.1406) .. controls
					(82.8906,42.1406) and (82.9102,48.1602) .. (82.9102,48.1875) .. controls
					(82.9102,48.2734) and (82.9648,48.3164) .. (83.0742,48.3164) --
					(84.3516,48.3164) .. controls (84.4570,48.3164) and (84.5195,48.2734) ..
					(84.5391,48.1836) -- (84.5391,43.9414) -- (84.6484,43.7852) .. controls
					(84.9297,43.4883) and (85.3203,43.3437) .. (85.5898,43.3398) .. controls
					(85.8203,43.3359) and (85.9336,43.3555) .. (86.0898,43.4258) .. controls
					(86.4883,43.6055) and (86.6719,43.9297) .. (86.6719,44.4062) --
					(86.6719,48.2305) .. controls (86.6875,48.2891) and (86.7422,48.3164) ..
					(86.8281,48.3164) -- (88.1055,48.3164) .. controls (88.2383,48.3164) and
					(88.3008,48.2500) .. (88.3008,48.1211) -- (88.3008,44.2227) .. controls
					(88.3008,43.6992) and (88.2109,43.2461) .. (88.0234,42.8789) .. controls
					(87.8438,42.5195) and (87.5938,42.2539) .. (87.2539,42.0625);
				\path[fill=TUMWhite,nonzero rule] (94.9883,42.4102) .. controls (94.9453,42.3906)
					and (94.6289,42.2305) .. (94.5859,42.2109) .. controls (94.0117,41.9258) and
					(93.4297,41.7812) .. (92.8477,41.7812) .. controls (92.1406,41.7812) and
					(91.5117,41.9258) .. (90.9805,42.2070) .. controls (90.4570,42.4844) and
					(90.0586,42.8672) .. (89.7695,43.3750) .. controls (89.4844,43.8750) and
					(89.3359,44.4492) .. (89.3359,45.1406) .. controls (89.3359,45.8320) and
					(89.4844,46.4180) .. (89.7695,46.9219) .. controls (90.0586,47.4258) and
					(90.4570,47.8086) .. (90.9805,48.0898) .. controls (91.5117,48.3711) and
					(92.1406,48.5117) .. (92.8477,48.5117) .. controls (93.4727,48.5117) and
					(94.0938,48.3477) .. (94.7070,48.0234) .. controls (94.7070,48.0234) and
					(94.7656,47.9961) .. (94.7852,47.9766) .. controls (94.8399,47.9336) and
					(94.8477,47.8711) .. (94.8203,47.7812) -- (94.4414,47.0156) .. controls
					(94.3828,46.9102) and (94.2969,46.8711) .. (94.1914,46.9062) .. controls
					(94.1875,46.9062) and (93.9883,46.9922) .. (93.8867,47.0234) .. controls
					(93.2227,47.2383) and (92.3672,47.1523) .. (91.8828,46.9023) .. controls
					(91.5781,46.7461) and (91.3359,46.4687) .. (91.1524,46.1758) .. controls
					(90.9727,45.8828) and (90.8828,45.5352) .. (90.8828,45.1445) .. controls
					(90.8828,44.7578) and (90.9727,44.4141) .. (91.1524,44.1211) .. controls
					(91.3359,43.8281) and (91.5781,43.5469) .. (91.8828,43.3945) .. controls
					(92.3672,43.1445) and (93.2734,43.0547) .. (93.9375,43.2695) .. controls
					(93.9922,43.2891) and (94.0664,43.3164) .. (94.1289,43.3437) .. controls
					(94.1914,43.3672) and (94.4883,43.5195) .. (94.4883,43.5195) .. controls
					(94.5977,43.5547) and (94.6797,43.5156) .. (94.7383,43.4102) --
					(95.0977,42.6562) .. controls (95.1289,42.5664) and (95.1172,42.5039) ..
					(95.0664,42.4570) .. controls (95.0430,42.4414) and (94.9883,42.4102) ..
					(94.9883,42.4102);
				\path[fill=TUMWhite,nonzero rule] (59.2188,19.4609) .. controls (59.4492,19.0391)
					and (59.5664,18.5391) .. (59.5664,17.9531) -- (59.5664,12.3281) .. controls
					(59.5703,12.3125) and (59.5703,12.2930) .. (59.5703,12.2617) .. controls
					(59.5703,12.1836) and (59.5195,12.1445) .. (59.4180,12.1445) --
					(57.2695,12.1445) .. controls (57.1484,12.1445) and (57.0859,12.2070) ..
					(57.0859,12.3281) -- (57.0859,17.6992) .. controls (57.0625,17.9492) and
					(56.9727,18.1445) .. (56.8203,18.2891) .. controls (56.6680,18.4297) and
					(56.4531,18.5039) .. (56.1758,18.5039) .. controls (55.8906,18.5039) and
					(55.6133,18.4023) .. (55.3516,18.1992) .. controls (55.3047,18.1641) and
					(55.2617,18.1445) .. (55.2266,18.1445) .. controls (55.1797,18.1445) and
					(55.1445,18.1797) .. (55.1211,18.2461) -- (54.5234,19.9141) .. controls
					(54.5195,19.9258) and (54.5195,19.9453) .. (54.5195,19.9687) .. controls
					(54.5195,20.0234) and (54.5469,20.0820) .. (54.6094,20.1367) .. controls
					(54.8359,20.3203) and (55.1328,20.4648) .. (55.5078,20.5781) .. controls
					(55.8828,20.6953) and (56.2617,20.7500) .. (56.6445,20.7500) .. controls
					(57.2578,20.7500) and (57.7812,20.6406) .. (58.2187,20.4180) .. controls
					(58.6562,20.1992) and (58.9883,19.8789) .. (59.2187,19.4609);
				\path[fill=TUMWhite,nonzero rule] (45.6523,44.6562) .. controls (45.6523,43.8477)
					and (46.3203,43.3359) .. (47.1641,43.3359) .. controls (47.9961,43.3359) and
					(48.5156,43.8477) .. (48.5156,44.6562) -- cycle(47.1797,41.7930) .. controls
					(46.6406,41.7930) and (45.2383,41.9531) .. (44.3594,43.3867) .. controls
					(44.0547,43.8906) and (43.9023,44.5703) .. (43.9023,45.1484) .. controls
					(43.9023,45.7305) and (44.0430,46.4414) .. (44.3711,46.9297) .. controls
					(45.0234,47.9023) and (46.0117,48.5078) .. (47.2734,48.5117) .. controls
					(48.1602,48.5156) and (49.2852,47.9648) .. (49.2852,47.9609) --
					(49.2852,47.9648) .. controls (49.3984,47.9141) and (49.4414,47.8281) ..
					(49.4023,47.7070) -- (49.0742,46.8555) .. controls (49.0117,46.7383) and
					(48.9219,46.7070) .. (48.8008,46.7617) .. controls (48.8008,46.7617) and
					(48.8008,46.7617) .. (48.7969,46.7617) .. controls (48.1445,46.9609) and
					(47.9805,47.1016) .. (47.2578,47.1016) .. controls (46.3672,47.1016) and
					(45.6523,46.4727) .. (45.6523,45.7578) -- (49.6328,45.7578) .. controls
					(49.7500,45.7422) and (49.8047,45.7148) .. (49.8398,45.5508) .. controls
					(49.9063,45.2500) and (49.9023,44.8984) .. (49.9023,44.7070) .. controls
					(49.9023,44.0273) and (49.7422,43.5273) .. (49.4727,43.0820) .. controls
					(48.8555,42.0547) and (47.7227,41.7930) .. (47.1797,41.7930);
				\path[fill=TUMWhite,nonzero rule] (43.0352,28.1328) -- (41.7578,28.1328) ..
					controls (41.6523,28.1328) and (41.5898,28.1758) .. (41.5703,28.2656) --
					(41.5703,32.5078) -- (41.4609,32.6641) .. controls (41.1797,32.9609) and
					(40.7891,33.1055) .. (40.5195,33.1094) .. controls (40.2891,33.1133) and
					(40.1719,33.0937) .. (40.0234,33.0234) .. controls (39.6211,32.8438) and
					(39.4375,32.5195) .. (39.4375,32.0430) -- (39.4375,28.2188) .. controls
					(39.4219,28.1641) and (39.3672,28.1328) .. (39.2812,28.1328) --
					(38.0039,28.1328) .. controls (37.8711,28.1328) and (37.8047,28.1992) ..
					(37.8047,28.3281) -- (37.8047,32.2266) .. controls (37.8047,32.7500) and
					(37.8984,33.2031) .. (38.0859,33.5742) .. controls (38.2656,33.9297) and
					(38.5156,34.1992) .. (38.8555,34.3867) .. controls (39.2031,34.5820) and
					(39.6992,34.6797) .. (39.9258,34.6797) .. controls (41.0000,34.6797) and
					(41.3164,34.1992) .. (41.7422,33.6836) .. controls (41.7422,33.6836) and
					(41.9727,34.3516) .. (41.9883,34.3750) .. controls (42.0352,34.4492) and
					(42.0898,34.4844) .. (42.1523,34.4844) -- (43.0039,34.4844) .. controls
					(43.0547,34.4844) and (43.0977,34.4648) .. (43.1367,34.4258) .. controls
					(43.1719,34.3867) and (43.1953,34.3477) .. (43.1953,34.3047) .. controls
					(43.1953,34.3047) and (43.1992,28.2891) .. (43.1992,28.2617) .. controls
					(43.1992,28.1758) and (43.1445,28.1328) .. (43.0351,28.1328);
				\path[fill=TUMWhite,nonzero rule] (42.5391,15.4102) .. controls (42.1484,15.1992)
					and (41.6836,15.0938) .. (41.1445,15.0938) .. controls (40.6562,15.1094) and
					(40.2461,15.2031) .. (39.9219,15.3672) -- (40.0273,14.3438) --
					(42.8242,14.3438) .. controls (42.9336,14.3438) and (43.0000,14.2852) ..
					(43.0195,14.1719) -- (43.2422,12.3047) .. controls (43.2422,12.1836) and
					(43.1836,12.1211) .. (43.0664,12.1211) -- (38.1055,12.1211) .. controls
					(37.9961,12.1211) and (37.9336,12.1836) .. (37.9180,12.3047) --
					(37.5781,17.0586) .. controls (37.5625,17.1836) and (37.6211,17.2461) ..
					(37.7578,17.2461) -- (40.2148,17.2461) .. controls (40.5234,17.2500) and
					(40.7656,17.3047) .. (40.9336,17.4062) .. controls (41.1055,17.5117) and
					(41.1914,17.6523) .. (41.1914,17.8359) .. controls (41.1914,18.0234) and
					(41.1055,18.1719) .. (40.9375,18.2812) .. controls (40.7695,18.3867) and
					(40.5312,18.4453) .. (40.2266,18.4453) .. controls (39.4414,18.4453) and
					(38.7539,18.2656) .. (38.1523,17.9062) .. controls (38.1289,17.8906) and
					(38.0898,17.8945) .. (38.0312,17.9140) .. controls (37.9766,17.9375) and
					(37.9414,17.9648) .. (37.9297,18.0039) -- (37.3359,19.6992) .. controls
					(37.3281,19.7148) and (37.3242,19.7383) .. (37.3242,19.7617) .. controls
					(37.3242,19.8125) and (37.3555,19.8555) .. (37.4180,19.8906) .. controls
					(38.3555,20.4570) and (39.3437,20.7383) .. (40.3828,20.7383) .. controls
					(41.0625,20.7383) and (41.6602,20.6211) .. (42.1641,20.3828) .. controls
					(42.6719,20.1445) and (43.0625,19.8086) .. (43.3320,19.3711) .. controls
					(43.6055,18.9375) and (43.7422,18.4219) .. (43.7422,17.8359) .. controls
					(43.7422,17.2461) and (43.6367,16.7500) .. (43.4297,16.3398) .. controls
					(43.2227,15.9297) and (42.9258,15.6211) .. (42.5391,15.4101);
				\path[fill=TUMWhite,nonzero rule] (74.5508,20.5078) .. controls (74.5898,20.4688)
					and (74.6055,20.4297) .. (74.6055,20.3789) -- (74.6055,15.9297) .. controls
					(74.6055,15.4609) and (74.5156,15.0547) .. (74.3281,14.7188) .. controls
					(74.1445,14.3828) and (73.8789,14.1250) .. (73.5352,13.9492) .. controls
					(73.1875,13.7695) and (72.7773,13.6836) .. (72.3008,13.6836) .. controls
					(71.5859,13.6836) and (71.0508,13.9102) .. (70.7031,14.3672) --
					(70.7031,11.8984) .. controls (70.6992,11.8477) and (70.6797,11.8047) ..
					(70.6445,11.7695) .. controls (70.6094,11.7344) and (70.5664,11.7148) ..
					(70.5195,11.7148) -- (68.3672,11.7148) .. controls (68.3203,11.7109) and
					(68.2774,11.7305) .. (68.2422,11.7695) .. controls (68.2070,11.8086) and
					(68.1875,11.8516) .. (68.1875,11.8984) -- (68.1875,20.3789) .. controls
					(68.1875,20.4336) and (68.2070,20.4766) .. (68.2422,20.5117) .. controls
					(68.2774,20.5469) and (68.3203,20.5664) .. (68.3672,20.5664) --
					(70.5195,20.5664) .. controls (70.5625,20.5664) and (70.6055,20.5469) ..
					(70.6445,20.5039) .. controls (70.6836,20.4648) and (70.7031,20.4258) ..
					(70.7031,20.3789) -- (70.7031,16.4648) -- (70.7500,16.2930) .. controls
					(70.7852,16.1641) and (70.8750,16.0469) .. (71.0156,15.9414) .. controls
					(71.1562,15.8320) and (71.3203,15.7813) .. (71.5078,15.7813) .. controls
					(71.9062,15.7813) and (72.1055,16.0352) .. (72.1055,16.5469) --
					(72.1055,20.3789) .. controls (72.0937,20.4297) and (72.1094,20.4687) ..
					(72.1484,20.5078) .. controls (72.1836,20.5469) and (72.2305,20.5664) ..
					(72.2773,20.5664) -- (74.4219,20.5664) .. controls (74.4687,20.5664) and
					(74.5117,20.5469) .. (74.5508,20.5078);
				\path[fill=TUMWhite,nonzero rule] (71.6289,39.6914) -- (70.3516,39.6914) ..
					controls (70.2461,39.6914) and (70.1797,39.7383) .. (70.1641,39.8242) --
					(70.1641,48.1875) .. controls (70.1641,48.2734) and (70.2188,48.3164) ..
					(70.3281,48.3164) -- (71.6055,48.3164) .. controls (71.7109,48.3164) and
					(71.7734,48.2734) .. (71.7930,48.1836) -- (71.7930,39.8203) .. controls
					(71.7930,39.7344) and (71.7383,39.6914) .. (71.6289,39.6914);
				\path[fill=TUMWhite,nonzero rule] (62.4453,42.4102) .. controls (62.4063,42.3906)
					and (62.0859,42.2305) .. (62.0430,42.2109) .. controls (61.4688,41.9258) and
					(60.8906,41.7812) .. (60.3047,41.7812) .. controls (59.5977,41.7812) and
					(58.9688,41.9258) .. (58.4414,42.2070) .. controls (57.9141,42.4844) and
					(57.5195,42.8672) .. (57.2305,43.3750) .. controls (56.9414,43.8750) and
					(56.7969,44.4492) .. (56.7969,45.1406) .. controls (56.7969,45.8320) and
					(56.9414,46.4180) .. (57.2305,46.9219) .. controls (57.5195,47.4258) and
					(57.9141,47.8086) .. (58.4414,48.0898) .. controls (58.9688,48.3711) and
					(59.5977,48.5117) .. (60.3047,48.5117) .. controls (60.9297,48.5117) and
					(61.5508,48.3477) .. (62.1641,48.0234) .. controls (62.1641,48.0234) and
					(62.2227,47.9961) .. (62.2422,47.9766) .. controls (62.2969,47.9336) and
					(62.3047,47.8711) .. (62.2774,47.7812) -- (61.8984,47.0156) .. controls
					(61.8399,46.9102) and (61.7578,46.8711) .. (61.6484,46.9062) .. controls
					(61.6445,46.9062) and (61.4492,46.9922) .. (61.3438,47.0234) .. controls
					(60.6797,47.2383) and (59.8281,47.1523) .. (59.3399,46.9023) .. controls
					(59.0391,46.7461) and (58.7930,46.4687) .. (58.6133,46.1758) .. controls
					(58.4297,45.8828) and (58.3399,45.5352) .. (58.3399,45.1445) .. controls
					(58.3399,44.7578) and (58.4297,44.4141) .. (58.6133,44.1211) .. controls
					(58.7930,43.8281) and (59.0391,43.5469) .. (59.3399,43.3945) .. controls
					(59.8281,43.1445) and (60.7344,43.0547) .. (61.3984,43.2695) .. controls
					(61.4492,43.2891) and (61.5234,43.3164) .. (61.5859,43.3437) .. controls
					(61.6484,43.3672) and (61.9453,43.5195) .. (61.9453,43.5195) .. controls
					(62.0547,43.5547) and (62.1406,43.5156) .. (62.1953,43.4102) --
					(62.5547,42.6562) .. controls (62.5859,42.5664) and (62.5742,42.5039) ..
					(62.5234,42.4570) .. controls (62.5039,42.4414) and (62.4453,42.4102) ..
					(62.4453,42.4102);
				\path[fill=TUMWhite,nonzero rule] (64.7227,44.6562) .. controls (64.7227,43.8477)
					and (65.3906,43.3359) .. (66.2305,43.3359) .. controls (67.0664,43.3359) and
					(67.5859,43.8477) .. (67.5859,44.6562) -- cycle(66.2500,41.7930) .. controls
					(65.7070,41.7930) and (64.3047,41.9531) .. (63.4297,43.3867) .. controls
					(63.1211,43.8906) and (62.9688,44.5703) .. (62.9688,45.1484) .. controls
					(62.9688,45.7305) and (63.1133,46.4414) .. (63.4414,46.9297) .. controls
					(64.0898,47.9023) and (65.0781,48.5078) .. (66.3438,48.5117) .. controls
					(67.2266,48.5156) and (68.3555,47.9648) .. (68.3516,47.9609) --
					(68.3555,47.9648) .. controls (68.4687,47.9141) and (68.5078,47.8281) ..
					(68.4687,47.7070) -- (68.1406,46.8555) .. controls (68.0781,46.7383) and
					(67.9883,46.7070) .. (67.8711,46.7617) .. controls (67.8711,46.7617) and
					(67.8672,46.7617) .. (67.8633,46.7617) .. controls (67.2109,46.9609) and
					(67.0469,47.1016) .. (66.3242,47.1016) .. controls (65.4336,47.1016) and
					(64.7227,46.4727) .. (64.7227,45.7578) -- (68.7031,45.7578) .. controls
					(68.8203,45.7422) and (68.8750,45.7148) .. (68.9102,45.5508) .. controls
					(68.9727,45.2500) and (68.9688,44.8984) .. (68.9688,44.7070) .. controls
					(68.9688,44.0273) and (68.8086,43.5273) .. (68.5430,43.0820) .. controls
					(67.9219,42.0547) and (66.7930,41.7930) .. (66.2500,41.7930);
			\end{scope}%
		\end{tikzpicture}%
	}%
}%
%
%
% >>> CONTENTS OF FILE source/FTM/Modules/FTMlogo.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%
\newcommand{\FTMlogoFTM}[5][!]{%
	\resizebox{#1}{#2}{%
		\FTMtikzExternalizeSkipNext%
		\begin{tikzpicture}[y=0.80pt, x=0.80pt, yscale=-1.000000, xscale=1.000000, inner sep=0pt, outer sep=0pt]
	\begin{scope}[cm={{1.33333,0.0,0.0,-1.33333,(0.0,37.81333)}}]
	\begin{scope}[scale=0.100]
		\path[fill=#3,nonzero rule] (81.8672,212.6910) -- (81.8672,277.6130) --
			(353.4770,277.6130) -- (353.4770,215.9060) .. controls (355.5200,214.8240) and
			(357.4610,213.5900) .. (359.4730,212.4530) -- (359.4730,283.6130) --
			(75.8594,283.6130) -- (75.8594,211.4610) .. controls (77.9219,211.9020) and
			(79.9414,212.3160) .. (81.8672,212.6910);
	\path[fill=#4,nonzero rule] (9.1719,105.4880) .. controls
			(15.3125,108.8670) and (23.6719,112.9880) .. (33.0469,116.3870) .. controls
			(33.0469,116.4690) and (33.0469,116.5200) .. (33.0469,116.6090) .. controls
			(33.2031,116.6020) and (33.4453,116.6090) .. (33.6133,116.6020) .. controls
			(36.5625,117.6560) and (39.5820,118.6480) .. (42.6758,119.4920) .. controls
			(57.0625,123.4220) and (66.4453,125.1800) .. (75.5273,126.8790) .. controls
			(79.8438,127.6880) and (84.0352,128.4770) .. (88.5664,129.4840) .. controls
			(91.1055,130.8360) and (93.6719,132.2620) .. (96.4258,133.8050) --
			(102.8200,137.3630) .. controls (112.7850,142.8240) and (149.7970,159.8010) ..
			(174.6600,163.3010) .. controls (185.5470,164.8360) and (200.3710,165.7540) ..
			(214.3160,165.7540) .. controls (220.1760,165.7540) and (225.2850,165.5740) ..
			(228.7110,165.2500) .. controls (326.3870,156.0940) and (350.2930,130.3280) ..
			(353.3590,126.4650) .. controls (353.7890,124.3360) and (354.0350,122.4060) ..
			(354.2110,120.5740) .. controls (360.7540,116.5350) and (367.1480,112.2620) ..
			(373.3130,107.5940) .. controls (377.3240,104.6020) and (379.7970,100.4690) ..
			(380.8200,95.5117) .. controls (381.2620,98.0781) and (381.5040,99.8164) ..
			(381.5040,99.8164) .. controls (383.3130,116.3550) and (382.6370,124.5230) ..
			(381.5230,134.9410) .. controls (381.4060,136.8090) and (381.0350,142.4920) ..
			(375.8400,146.3670) .. controls (333.1050,178.7300) and (280.9450,195.7460) ..
			(220.8400,196.9380) -- (216.2230,196.9840) .. controls (168.3010,196.9840) and
			(133.0860,182.1090) .. (112.0310,173.2230) .. controls (105.1760,170.3280) and
			(99.7656,168.0430) .. (96.2695,167.2660) .. controls (91.5547,166.2150) and
			(87.2266,165.4060) .. (82.7461,164.5660) .. controls (73.7695,162.8870) and
			(64.4922,161.1480) .. (50.3711,157.2890) .. controls (28.6719,151.3630) and
			(9.2188,138.5550) .. (8.3984,138.0120) -- (6.1133,136.4960) --
			(6.2305,130.4690) .. controls (6.6094,123.4380) and (7.6563,114.9880) ..
			(9.1719,105.4880);
		\path[fill=#5,nonzero rule] (388.8480,178.5270) .. controls
			(388.7300,180.3910) and (388.3710,186.0740) .. (383.1760,189.9530) .. controls
			(340.4300,222.3160) and (288.2810,239.3320) .. (228.1640,240.5230) --
			(223.5550,240.5660) .. controls (175.6370,240.5660) and (140.4100,225.6950) ..
			(119.3670,216.8090) .. controls (112.5120,213.9100) and (107.0900,211.6250) ..
			(103.5940,210.8520) .. controls (98.8867,209.8010) and (94.5508,208.9920) ..
			(90.0781,208.1520) .. controls (81.1055,206.4690) and (71.8281,204.7340) ..
			(57.6953,200.8750) .. controls (35.9961,194.9490) and (16.5430,182.1410) ..
			(15.7305,181.5980) -- (13.4375,180.0780) -- (13.5547,174.0550) .. controls
			(13.9375,167.1640) and (14.9336,158.9300) .. (16.4063,149.6720) .. controls
			(24.5703,154.0940) and (36.1836,159.6330) .. (48.7891,163.0780) .. controls
			(63.1758,167.0080) and (72.5586,168.7660) .. (81.6406,170.4650) .. controls
			(86.0547,171.2890) and (90.3203,172.0900) .. (94.9727,173.1250) .. controls
			(95.6055,173.2700) and (96.3984,173.5120) .. (97.2344,173.7890) .. controls
			(99.3477,174.9380) and (101.4840,176.1170) .. (103.7500,177.3870) --
			(110.1560,180.9490) .. controls (120.1170,186.4060) and (157.1290,203.3830) ..
			(181.9920,206.8870) .. controls (192.8830,208.4180) and (207.7070,209.3360) ..
			(221.6480,209.3360) .. controls (227.5000,209.3360) and (232.6170,209.1560) ..
			(236.0350,208.8320) .. controls (333.7110,199.6800) and (357.6290,173.9100) ..
			(360.6910,170.0510) .. controls (361.1840,167.6330) and (361.4380,165.4610) ..
			(361.6020,163.4220) .. controls (367.7070,159.6020) and (373.6640,155.5430) ..
			(379.4260,151.1760) .. controls (384.3670,147.4960) and (387.0820,142.1600) ..
			(387.4920,135.5820) .. controls (387.4920,135.5470) and (387.5000,135.5120) ..
			(387.5000,135.4730) .. controls (388.3520,139.9020) and (388.8400,143.3980) ..
			(388.8400,143.3980) .. controls (390.6450,159.9380) and (389.9610,168.1050) ..
			(388.8480,178.5270);
		\path[fill=#3,nonzero rule] (369.7270,102.7850) .. controls
			(326.9920,135.1480) and (274.8360,152.1640) .. (214.7270,153.3550) --
			(210.1050,153.3980) .. controls (162.1880,153.3980) and (126.9730,138.5270) ..
			(105.9180,129.6410) .. controls (99.0625,126.7420) and (93.6523,124.4570) ..
			(90.1563,123.6840) .. controls (85.4414,122.6330) and (81.1133,121.8240) ..
			(76.6328,120.9840) .. controls (67.6563,119.3010) and (58.3789,117.5660) ..
			(44.2578,113.7070) .. controls (22.5586,107.7810) and (3.1055,94.9727) ..
			(2.2852,94.4297) -- (0.0000,92.9102) -- (0.1172,86.8867) .. controls
			(0.8125,74.1523) and (3.4961,57.1328) .. (7.7070,36.6914) .. controls
			(10.7930,21.6953) and (14.6211,10.2344) .. (19.4336,9.9336) .. controls
			(24.8359,9.5898) and (28.7500,51.2695) .. (28.7500,51.2695) .. controls
			(28.7500,51.2695) and (27.8438,56.3398) .. (27.3750,62.2773) .. controls
			(26.9023,68.2148) and (27.0508,64.9063) .. (26.9336,73.0234) .. controls
			(31.8164,72.8867) and (40.3594,73.0000) .. (51.3398,74.9492) .. controls
			(68.4844,77.9883) and (77.6367,83.1211) .. (90.3125,90.2188) --
			(96.7109,93.7813) .. controls (106.6720,99.2383) and (143.6840,116.2150) ..
			(168.5470,119.7190) .. controls (179.4340,121.2500) and (194.2580,122.1680) ..
			(208.2030,122.1680) .. controls (214.0630,122.1680) and (219.1720,121.9880) ..
			(222.5980,121.6640) .. controls (320.2730,112.5120) and (344.1800,86.7422) ..
			(347.2460,82.8828) .. controls (349.8050,70.1953) and (347.2460,62.4805) ..
			(347.2270,62.4375) -- (346.3280,59.9492) .. controls (346.3280,59.9492) and
			(360.3590,29.7773) .. (366.9730,30.0781) .. controls (371.7970,30.2969) and
			(375.3910,56.2305) .. (375.3910,56.2305) .. controls (377.1950,72.7695) and
			(376.5230,80.9375) .. (375.4100,91.3594) .. controls (375.2930,93.2227) and
			(374.9220,98.9063) .. (369.7270,102.7850);
		\path[fill=#3,nonzero rule] (353.4770,6.0117) -- (81.8672,6.0117) --
			(81.8672,78.8438) .. controls (79.9023,77.8516) and (77.9102,76.9023) ..
			(75.8594,76.0078) -- (75.8594,0.0000) -- (359.4730,0.0000) --
			(359.4730,27.5664) .. controls (357.7660,29.1172) and (355.7810,31.3477) ..
			(353.4770,34.6250) -- (353.4770,6.0117);
		\path[fill=#3,nonzero rule] (81.8672,277.6130) -- (353.4770,277.6130) --
			(353.4770,215.9060) .. controls (355.5200,214.8240) and (357.4610,213.5900) ..
			(359.4730,212.4530) -- (359.4730,283.6130) -- (75.8594,283.6130) --
			(75.8594,211.4610) .. controls (77.9219,211.9020) and (79.9414,212.3160) ..
			(81.8672,212.6910) -- (81.8672,277.6130);
	\end{scope}
	\end{scope}
	\end{tikzpicture}%
	}%
}%
%
%
%
\else\fi% End-check if module FTMlogo is enabled
%###################################################################################################
%--- END MODULE FTMlogo ----------------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- BEGIN MODULE FTMmath --------------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMmath% Start-check if module FTMmath is enabled
%
% >>> CONTENTS OF FILE source/TUM/Modules/TUMmath.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%===============================
%--- Default Option handling ---
%===============================
% Select left aligned equations, if no other option is given
\ifdefined\optLeftEquations\else%
\ifdefined\optCenterEquations\else%
	\def\optLeftEquations{x}%
\fi%
\fi%
%
%
%================
%--- Packages ---
%================
\ifdefined\optLeftEquations%
	\PassOptionsToPackage{fleqn}{amsmath}%
\fi%
\RequirePackage{amsmath}%
\RequirePackage{mathtools}%
\RequirePackage{siunitx}%
\RequirePackage{upgreek}%
\ifdefined\optComputerModernMath% in this case the mathdesign package has not been loaded
	\RequirePackage{amssymb}%
	\RequirePackage{amsfonts}%
\else\fi%
%
%===================
%--- Definitions ---
%===================
% Math operators
% --------------
\DeclareMathOperator{\real}{Re}%
\DeclareMathOperator{\imag}{Im}%
\DeclareMathOperator{\asin}{asin}%
\DeclareMathOperator{\acos}{acos}%
\DeclareMathOperator{\atan}{atan}%
\DeclareMathOperator{\co}{co}%
\DeclareMathOperator{\atanII}{atan2}%
\DeclareMathOperator{\AtanII}{Atan2}%
\DeclareMathOperator{\sinabr}{s}%
\DeclareMathOperator{\cosabr}{c}%
\DeclareMathOperator{\sign}{sign}%
\let\sgn\relax%
\DeclareMathOperator{\sgn}{sgn}%
\DeclareMathOperator{\argmin}{arg\,min}%
\DeclareMathOperator{\argmax}{arg\,max}%
\let\div\undefined%
\DeclareMathOperator{\div}{div}%
\DeclareMathOperator{\grad}{grad}%
\DeclareMathOperator{\dif}{d \!}%
\DeclareMathOperator{\Dif}{D \!}%
\DeclareMathOperator{\order}{O}%
%
% Misc
% ----
\newcommand{\Abs}[1]{\mathinner{\left\vert#1\right\vert}}%
\newcommand{\abs}[1]{\mathinner{\vert#1\vert}}%
\newcommand{\Norm}[1]{\mathinner{\left\Vert#1\right\Vert}}%
\newcommand{\norm}[1]{\mathinner{\Vert#1\Vert}}%
\newcommand{\e}{\ensuremath{\mathalpha{\mathrm{e}}}}%
\newcommand{\const}{\mbox{const}}%
\newcommand{\konst}{\mbox{konst}}%
\newcommand{\laplacian}{\Delta}%
%
% Numeral system
% --------------
\newcommand{\hex}[1]{\mathalpha{\mathtt{#1}_\mathrm{H}}}%
\newcommand{\bin}[1]{\mathalpha{\mathtt{#1}_\mathrm{B}}}%
\newcommand{\dec}[1]{\mathalpha{\mathtt{#1}_\mathrm{D}}}%
\newcommand{\bnot}[1]{\mathalpha{\overline{\mbox{$#1$}}}}%
%
% Sets of numbers
% ---------------
\newcommand{\MR}{\ensuremath{\mathalpha{\mathbb{R}}}}%
\newcommand{\MN}{\ensuremath{\mathalpha{\mathbb{N}}}}%
\newcommand{\MZ}{\ensuremath{\mathalpha{\mathbb{Z}}}}%
\newcommand{\MC}{\ensuremath{\mathalpha{\mathbb{C}}}}%
\newcommand{\MQ}{\ensuremath{\mathalpha{\mathbb{Q}}}}%
\newcommand{\Mone}{\ensuremath{\mathalpha{\mathbb{1}}}}%
%
% Relations
% ---------
\newcommand{\eqhat}{\mathrel{\widehat{=}}}%
\newcommand{\eqexcl}{\stackrel{!}{=}}%
\newcommand{\eqdef}{\stackrel{\mathrm{def.}}{=}}%
\newcommand{\defined}{\coloneqq}%
\newcommand{\rdefined}{\eqqcolon}%
%
% Vectors and matrices
% --------------------
% vectors (main definition)
\let\origvec\vec%
\let\vec\relax%
\newcommand{\vec}[1]{\ensuremath{\boldsymbol{#1}}}%
%
% vectors (latin letters lower case)
\def\vecdeflatinlower#1{\expandafter\def\csname v#1\endcsname{\vec{#1}}}%
\def\vecdeflatinlowerall#1{\ifx#1\vecdeflatinlowerall\else\vecdeflatinlower{#1}\expandafter\vecdeflatinlowerall\fi}%
\vecdeflatinlowerall abcdefghijklmnopqrstuvwxyz\vecdeflatinlowerall%
%
% vectors (latin letters upper case)
\def\vecdeflatinupper#1{\expandafter\def\csname v#1\endcsname{\vec{#1}}}%
\def\vecdeflatinupperall#1{\ifx#1\vecdeflatinupperall\else\vecdeflatinupper{#1}\expandafter\vecdeflatinupperall\fi}%
\vecdeflatinupperall ABCDEFGHIJKLMNOPQRSTUVWXYZ\vecdeflatinupperall%
%
% vectors (greek letters lower case)
\def\vecdefgreeklower#1{\expandafter\def\csname v#1\endcsname{\vec{\csname #1\endcsname}}}%
\def\vecdefgreeklowerall#1{\ifx#1\vecdefgreeklowerall\else\vecdefgreeklower{#1}\expandafter\vecdefgreeklowerall\fi}%
\vecdefgreeklowerall {alpha}{beta}{gamma}{delta}{epsilon}{varepsilon}{zeta}{eta}{theta}{vartheta}{iota}{kappa}{lambda}{mu}{nu}{pi}{varpi}%
{xi}{rho}{varrho}{sigma}{varsigma}{tau}{upsilon}{phi}{varphi}{chi}{psi}{omega}\vecdefgreeklowerall%
%
% vectors (greek letters upper case)
\def\vecdefgreekupper#1{\expandafter\def\csname v#1\endcsname{\vec{\csname #1\endcsname}}}%
\def\vecdefgreekupperall#1{\ifx#1\vecdefgreekupperall\else\vecdefgreekupper{#1}\expandafter\vecdefgreekupperall\fi}%
\vecdefgreekupperall {Gamma}{Delta}{Theta}{Lambda}{Xi}{Pi}{Sigma}{Upsilon}{Phi}{Psi}{Omega}\vecdefgreekupperall%
%
% vectors (misc)
\newcommand{\vnull}{\vec{0}}%
\newcommand{\vzero}{\vec{0}}%
\newcommand{\vone}{\vec{1}}%
%
% matrices
\newcommand{\mat}[1]{\begin{matrix}#1\end{matrix}}%
\newcommand{\pmat}[1]{\begin{pmatrix}#1\end{pmatrix}}%
\newcommand{\bmat}[1]{\begin{bmatrix}#1\end{bmatrix}}%
\newcommand{\Bmat}[1]{\begin{Bmatrix}#1\end{Bmatrix}}%
\newcommand{\vmat}[1]{\begin{vmatrix}#1\end{vmatrix}}%
\newcommand{\Vmat}[1]{\begin{Vmatrix}#1\end{Vmatrix}}%
%
% Derivatives
% -----------
\newcommand{\dd}[1]{\dif #1}%
\newcommand{\vdot}[1]{\vec{\dot{#1}}}%
\newcommand{\vddot}[1]{\vec{\ddot{#1}}}%
\newcommand{\diff}[3][]{\frac{\mathrm{d}^{#1}\,\!#2}{\mathrm{d}\,\!{#3}^{#1}}}%
\newcommand{\tdiff}[3][]{\tfrac{\mathrm{d}^{#1}\,\!#2}{\mathrm{d}\,\!{#3}^{#1}}}%
\newcommand{\pdiff}[3][]{\frac{\partial^{#1}\,\!#2}{\partial\,\!#3^{#1}}}%
\newcommand{\tpdiff}[3][]{\tfrac{\partial^{#1}\,\!#2}{\partial\,\!#3^{#1}}}%
\newcommand{\Ddiff}[3][]{\frac{D^{#1}\,\!#2}{D\,\!#3^{#1}}}%
\newcommand{\tDdiff}[3][]{\frac{D^{#1}\,\!#2}{D\,\!#3^{#1}}}%
%
% Accents
% -------
% Declare new symbol font for non-bold accents
\DeclareSymbolFont{nbaccents}{OT1}{cmr}{m}{n}%
% Set accents in math mode to use non-bold font
\DeclareMathAccent{\acute}{\mathord}{nbaccents}{"13}%
\DeclareMathAccent{\bar}{\mathord}{nbaccents}{"16}%
\DeclareMathAccent{\breve}{\mathord}{nbaccents}{"15}%
\DeclareMathAccent{\check}{\mathord}{nbaccents}{"14}%
\DeclareMathAccent{\dot}{\mathord}{nbaccents}{"5F}%
\DeclareMathAccent{\ddot}{\mathord}{nbaccents}{"7F}%
\DeclareMathAccent{\grave}{\mathord}{nbaccents}{"12}%
\DeclareMathAccent{\hat}{\mathord}{nbaccents}{"5E}%
\DeclareMathAccent{\tilde}{\mathord}{nbaccents}{"7E}%
%
%
% Indices
% -------
\def\rs#1{\@ifnextchar[%]
  {\@rs{#1}}{\@@rs{#1}}}%
\def\@rs#1[#2]#3{\mathinner{%
	\setbox\@ne\hbox{$\displaystyle{\vphantom{#3}}#1{#3}\m@th$}%
	\setbox\tw@\hbox{$\displaystyle{#3}#2\m@th$}%
	\hskip\wd\@ne\hskip-\wd\tw@\mathord{\hskip\wd\tw@\hskip-\wd\@ne%
	  {\vphantom{#3}}#1{#3}#2}}}%
\def\@@rs#1#2{\mathinner{%
	\setbox\@ne\hbox{$\displaystyle{\vphantom{#2}}#1{#2}\m@th$}%
	\hskip\wd\@ne\mathord{\hskip-\wd\@ne%
	  {\vphantom{#2}}#1{#2}}}}%
%
%
% >>> CONTENTS OF FILE source/FTM/Modules/FTMmath.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%
%
% Units
%
\RequirePackage{siunitx}%
\ifdefined\optGerman% Customize SIrange-command for german language
\sisetup{%
	output-decimal-marker={,},%
	exponent-product=\cdot,%
	range-phrase=\text{ bis },%
	list-final-separator=\text{ und },%
	number-unit-product=~,%
	per-mode=fraction,%
	inter-unit-product=\,%
}%
% setup for typo in FTMPreText
\else\fi%
%
%
\else\fi% End-check if module FTMmath is enabled
%###################################################################################################
%--- END MODULE FTMmath ----------------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- BEGIN MODULE FTMlayout ------------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMlayout% Start-check if module FTMlayout is enabled
%
% >>> CONTENTS OF FILE source/TUM/Modules/TUMlayout.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%===============================
%--- Default Option Handling ---
%===============================
% Select A4-size, if no option has been passed
\ifdefined\optAfour\else%
\ifdefined\optAzero\else%
\ifdefined\optBeamerClassicFormat\else%
\ifdefined\optBeamerWideFormat\else%
	\def\optAfour{x}%
\fi%
\fi%
\fi%
\fi%
%
%================
%--- Packages ---
%================
\ifdefined\optAfour%
	\RequirePackage{geometry}%
	\geometry{a4paper, margin=2cm}%
\fi%
\ifdefined\optAzero%
	\RequirePackage{geometry}%
	\geometry{a0paper, margin=2cm}%
\fi%
\ifdefined\optBeamerClassicFormat%
	\RequirePackage{geometry}%
	\geometry{paperwidth=25.4cm, paperheight=19.05cm, left=1cm, right=1cm}%
\fi%
\ifdefined\optBeamerWideFormat%
	\RequirePackage{geometry}%
	\geometry{paperwidth=25.4cm, paperheight=14.29cm, left=1cm, right=1cm}%
\fi%
%
%
%=============
%--- Style ---
%=============
\newlength{\FTMlayoutHeaderSize}%       Factor to specify the scaling of header elements
\setlength{\FTMlayoutHeaderSize}{1cm}%  Default factor
\ifdefined\optAzero%
	\setlength{\FTMlayoutHeaderSize}{4cm}%
\fi%
%
%
%================
%--- Commands ---
%================
% Set document format
% -------------------
\newcommand{\FTMlayoutSetAfour}{%
	\def\optAfour{x}%
	\undef\optAzero%
	\undef\optBeamerClassicFormat%
	\undef\optBeamerWideFormat%
	\geometry{a4paper}%
}%
\newcommand{\FTMlayoutSetAzero}{%
	\undef\optAfour%
	\def\optAzero{x}%
	\undef\optBeamerClassicFormat%
	\undef\optBeamerWideFormat%
	\geometry{a0paper}%
}%
\newcommand{\FTMlayoutSetBeamerClassicFormat}{%
	\undef\optAfour%
	\undef\optAzero%
	\def\optBeamerClassicFormat{x}%
	\undef\optBeamerWideFormat%
	\geometry{paperwidth=25.4cm, paperheight=19.05cm}%
}%
\newcommand{\FTMlayoutSetBeamerWideFormat}{%
	\undef\optAfour%
	\undef\optAzero%
	\undef\optBeamerClassicFormat%
	\def\optBeamerWideFormat{x}%
	\geometry{paperwidth=25.4cm, paperheight=14.29cm}%
}%
%
% Absolute positioning on page
% ----------------------------
\newcommand{\FTMlayoutPutAtCenter}[2][0]{%
	\FTMtikzExternalizeSkipNext%
	\begin{tikzpicture}[remember picture, overlay]%
		\node[shift={($ (\paperwidth/2,\paperheight/2) $)},outer sep=0,inner sep=0,rotate=#1,align=left] at (current page.south west) {#2};%
	\end{tikzpicture}%
}%
\newcommand{\FTMlayoutPutAtNorthWest}[4][0]{%
	\FTMtikzExternalizeSkipNext%
	\begin{tikzpicture}[remember picture, overlay]%
		\node[shift={(#2,-#3)},outer sep=0,inner sep=0,anchor = north west,rotate=#1,align=left] at (current page.north west) {#4};%
	\end{tikzpicture}%
}%
\newcommand{\FTMlayoutPutAtNorthWestCentered}[4][0]{%
	\FTMtikzExternalizeSkipNext%
	\begin{tikzpicture}[remember picture, overlay]%
		\node[shift={(#2,-#3)},outer sep=0,inner sep=0,rotate=#1,align=left] at (current page.north west) {#4};%
	\end{tikzpicture}%
}%
\newcommand{\FTMlayoutPutAtNorthEast}[4][0]{%
	\FTMtikzExternalizeSkipNext%
	\begin{tikzpicture}[remember picture, overlay]%
		\node[shift={(-#2,-#3)},outer sep=0,inner sep=0,anchor = north east,rotate=#1,align=left] at (current page.north east) {#4};%
	\end{tikzpicture}%
}%
\newcommand{\FTMlayoutPutAtNorthEastCentered}[4][0]{%
	\FTMtikzExternalizeSkipNext%
	\begin{tikzpicture}[remember picture, overlay]%
		\node[shift={(-#2,-#3)},outer sep=0,inner sep=0,rotate=#1,align=left] at (current page.north east) {#4};%
	\end{tikzpicture}%
}%
\newcommand{\FTMlayoutPutAtSouthWest}[4][0]{%
	\FTMtikzExternalizeSkipNext%
	\begin{tikzpicture}[remember picture, overlay]%
		\node[shift={(#2,#3)},outer sep=0,inner sep=0,anchor = south west,rotate=#1,align=left] at (current page.south west) {#4};%
	\end{tikzpicture}%
}%
\newcommand{\FTMlayoutPutAtSouthWestCentered}[4][0]{%
	\FTMtikzExternalizeSkipNext%
	\begin{tikzpicture}[remember picture, overlay]%
		\node[shift={(#2,#3)},outer sep=0,inner sep=0,rotate=#1,align=left] at (current page.south west) {#4};%
	\end{tikzpicture}%
}%
\newcommand{\FTMlayoutPutAtSouthEast}[4][0]{%
	\FTMtikzExternalizeSkipNext%
	\begin{tikzpicture}[remember picture, overlay]%
		\node[shift={(-#2,#3)},outer sep=0,inner sep=0,anchor = south east,rotate=#1,align=left] at (current page.south east) {#4};%
	\end{tikzpicture}%
}%
\newcommand{\FTMlayoutPutAtSouthEastCentered}[4][0]{%
	\FTMtikzExternalizeSkipNext%
	\begin{tikzpicture}[remember picture, overlay]%
		\node[shift={(-#2,#3)},outer sep=0,inner sep=0,rotate=#1,align=left] at (current page.south east) {#4};%
	\end{tikzpicture}%
}%
%
% Headers
% -------
\newcommand{\FTMlayoutHeaderCDTUMLogoOnly}[1][TUMAnniGreen2]{%
	% Output TUM logo
	\FTMlayoutPutAtNorthEast{\FTMlayoutHeaderSize}{\FTMlayoutHeaderSize}{\FTMlogoTUM{\FTMlayoutHeaderSize}{TUMBlue}}%
	% Output anniversary badge
	\ifdefined\optExzellenz%
		\FTMlayoutPutAtNorthEast{3.9\FTMlayoutHeaderSize}{0cm}{\FTMlogoAnniversary[\FTMlayoutHeaderSize]{#1}}%
	\fi%
}%
\newcommand{\FTMlayoutHeaderCDTUM}[1][TUMAnniGreen2]{%
	% Output TUM tercet
	\FTMlayoutPutAtNorthWest{\FTMlayoutHeaderSize}{\FTMlayoutHeaderSize}{\FTMlogoTercetTUM{\FTMlayoutHeaderSize}}%
	% Output TUM logo
	\FTMlayoutPutAtNorthEast{\FTMlayoutHeaderSize}{\FTMlayoutHeaderSize}{\FTMlogoTUM{\FTMlayoutHeaderSize}{TUMBlue}}%
	% Output anniversary badge
	\ifdefined\optExzellenz%
		\FTMlayoutPutAtNorthEast{3.9\FTMlayoutHeaderSize}{0cm}{\FTMlogoAnniversary[\FTMlayoutHeaderSize]{#1}}%
	\fi%
}%
\newcommand{\FTMlayoutHeaderCDDepartment}[1][TUMAnniGreen2]{%
	% Output department logo
	\FTMlayoutPutAtNorthWest{\FTMlayoutHeaderSize}{\FTMlayoutHeaderSize}{\FTMlogoDepartment{\FTMlayoutHeaderSize}{TUMBlue}}%
	% Output TUM tercet
	\FTMlayoutPutAtNorthWest{2.7\FTMlayoutHeaderSize}{\FTMlayoutHeaderSize}{\FTMlogoTercetDepartment{\FTMlayoutHeaderSize}}%
	% Output TUM logo
	\FTMlayoutPutAtNorthEast{\FTMlayoutHeaderSize}{\FTMlayoutHeaderSize}{\FTMlogoTUM{\FTMlayoutHeaderSize}{TUMBlue}}%
	% Output anniversary badge
	\ifdefined\optExzellenz%
		\FTMlayoutPutAtNorthEast{3.9\FTMlayoutHeaderSize}{0cm}{\FTMlogoAnniversary[\FTMlayoutHeaderSize]{#1}}%
	\fi%
}%
\newcommand{\FTMlayoutHeaderCDChair}[1][TUMAnniGreen2]{%
	% Output TUM tercet
	\FTMlayoutPutAtNorthWest{\FTMlayoutHeaderSize}{\FTMlayoutHeaderSize}{\FTMlogoTercetChair{\FTMlayoutHeaderSize}}%
	% Output TUM logo
	\FTMlayoutPutAtNorthEast{\FTMlayoutHeaderSize}{\FTMlayoutHeaderSize}{\FTMlogoTUM{\FTMlayoutHeaderSize}{TUMBlue}}%
	% Output anniversary badge
	\ifdefined\optExzellenz%
		\FTMlayoutPutAtNorthEast{3.9\FTMlayoutHeaderSize}{0cm}{\FTMlogoAnniversary[\FTMlayoutHeaderSize]{#1}}%
	\fi%
}%
%
% Debugging
% ---------
\newcommand{\FTMlayoutCDBorder}{%
	\FTMlayoutPutAtNorthWest{0cm}{0cm}{%
		\begin{tikzpicture}%
			\draw [red] (\FTMlayoutHeaderSize,0cm) -- (\FTMlayoutHeaderSize,\paperheight);%
			\draw [red] (\paperwidth-\FTMlayoutHeaderSize,0cm) -- (\paperwidth-\FTMlayoutHeaderSize,\paperheight);%
			\draw [red] (0cm,\FTMlayoutHeaderSize) -- (\paperwidth,\FTMlayoutHeaderSize);%
			\draw [red] (0cm,\paperheight-\FTMlayoutHeaderSize) -- (\paperwidth,\paperheight-\FTMlayoutHeaderSize);%
			\draw [red] (0cm,\paperheight-2\FTMlayoutHeaderSize) -- (\paperwidth,\paperheight-2\FTMlayoutHeaderSize);%
			\draw [red] (0cm,\paperheight-3\FTMlayoutHeaderSize) -- (\paperwidth,\paperheight-3\FTMlayoutHeaderSize);%
			\draw [red] (\paperwidth-2.9\FTMlayoutHeaderSize,\paperheight-3\FTMlayoutHeaderSize) -- (\paperwidth-2.9\FTMlayoutHeaderSize,\paperheight);%
			\draw [red] (\paperwidth-3.9\FTMlayoutHeaderSize,\paperheight-3\FTMlayoutHeaderSize) -- (\paperwidth-3.9\FTMlayoutHeaderSize,\paperheight);%
		\end{tikzpicture}%
	}%
}%
%
%
% >>> CONTENTS OF FILE source/FTM/Modules/FTMlayout.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%
%================
%--- Packages ---
%================
%
\RequirePackage{pdfpages}%
% Appendix
\RequirePackage{appendix}%
\ifdefined\optGerman%
	\renewcommand{\appendixname}{Anhang}%
\else%
\fi%
%
\ifdefined\optFTMstudentthesis%
	\RequirePackage{setspace}%
	\setstretch{1.08}%
\else%
	\ifdefined\optFTMphdthesis%
		\RequirePackage{setspace}%
	\setstretch{1.08}%
\fi%
\fi%
%
%
%================
%--- Commands ---
%================
% Headers
% -------
% Custom design (chair)
\newcommand{\FTMlayoutHeaderCustomChair}{%
	\ifdefined\optAzero%
		%\FTMlayoutPutAtNorthWest{4cm}{3.5cm}{\FTMlogoFTM{4.6cm}{FTMLogoBlue1}{FTMLogoBlue2}}%
		\FTMlayoutPutAtNorthWest{9cm}{4cm}{\FTMlogoTercetChair{4cm}}%
		\FTMlayoutPutAtNorthEast{4cm}{4cm}{\FTMlogoTUM{4cm}{TUMBlue}}%
	\else%
		\ifdefined\optAfour%
			%\FTMlayoutPutAtNorthWest{2cm}{1.35cm}{\FTMlogoFTM{1.15cm}{FTMLogoBlue1}{FTMLogoBlue2}}%
			\FTMlayoutPutAtNorthWest{3.2cm}{1.5cm}{\FTMlogoTercetChair{1cm}}%
			\FTMlayoutPutAtNorthEast{2cm}{1.5cm}{\FTMlogoTUM{1cm}{TUMBlue}}%
		\else%
			%\FTMlayoutPutAtNorthWest{1cm}{0.85cm}{\FTMlogoFTM{1.15cm}{FTMLogoBlue1}{FTMLogoBlue2}}%
			\FTMlayoutPutAtNorthWest{2.2cm}{1cm}{\FTMlogoTercetChair{1cm}}%
			\FTMlayoutPutAtNorthEast{1cm}{1cm}{\FTMlogoTUM{1cm}{TUMBlue}}%
		\fi%
	\fi%
}%
%
%
% Title pages
% -----------
\newcommand{\FTMTitlePageDefault}[3]{%
	\FTMlayoutHeaderCustomChair%
	\vskip1.6cm\noindent%
	\ifx\\#1\\\else%    %check, if argument is not empty
		\textbf{\huge #1}%
	\fi%
	\ifx\\#2\\\else%    %check, if argument is not empty
		\\[1em]\textbf{\Large \color{TUMBlue} #2}%
	\fi%
	\ifx\\#3\\\else%    %check, if argument is not empty
		\\[1em]#3%
	\fi%
	\par%
}%
%
%
%
\else\fi% End-check if module FTMlayout is enabled
%###################################################################################################
%--- END MODULE FTMlayout --------------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- BEGIN MODULE FTMbiblio ------------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMbiblio% Start-check if module FTMbiblio is enabled
%
% >>> CONTENTS OF FILE source/TUM/Modules/TUMbiblio.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%=======================
%--- Option handling ---
%=======================
% Check, if a backend has been specified
\ifdefined\optBiber%
	\def\BackendSpecified{x}%
\else\fi%
\ifdefined\optBibtex%
	\def\BackendSpecified{x}%
\else\fi%
%
% Use numeric citation style as default
\ifdefined\optBibstyleNumeric\else%
\ifdefined\optBibstyleAlphabetic\else%
\ifdefined\optBibstyleAuthorYear\else%
	\def\optBibstyleNumeric{x}%
\fi%
\fi%
\fi%
%
%
% Perform rest only, if a backend has been specified
\ifdefined\BackendSpecified%
%================
%--- Packages ---
%================
% Select backend
% --------------
\ifdefined\optBiber% Load biblatex package with biber as backend
	\PassOptionsToPackage{backend=biber}{biblatex}%
\else\fi%
\ifdefined\optBibtex% Load biblatex package with bibtex as backend
	\PassOptionsToPackage{backend=bibtex}{biblatex}%
\else\fi%
%
% Select citation style
% ---------------------
\ifdefined\optBibstyleNumeric%
	\PassOptionsToPackage{style=numeric-comp}{biblatex}%
\else\fi%
\ifdefined\optBibstyleAlphabetic%
	\PassOptionsToPackage{style=alphabetic}{biblatex}%
\else\fi%
\ifdefined\optBibstyleAuthorYear%
	\PassOptionsToPackage{style=authoryear-comp}{biblatex}%
\else\fi%
%
% Load package
% ------------
\RequirePackage{biblatex}%
%
% Set options
% -----------
% Abbreviate first name with inits
\@ifpackagelater{biblatex}{2016/03/13}%
{%
	\ExecuteBibliographyOptions{giveninits=true}% new option
}%
{%
	\ExecuteBibliographyOptions{firstinits=true}% deprecated option
}%
%
% Sorting
% -------
\ExecuteBibliographyOptions{sorting=none}% Set sorting order
\DeclareNameAlias{sortname}{last-first}%  Sort by last name
\DeclareNameAlias{default}{last-first}%   Print last name first
%
%
% End test, if a backend has been specified
\else\fi%
%
%
% >>> CONTENTS OF FILE source/FTM/Modules/FTMbiblio.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%
%
%===================
%--- Bibliography ---
%===================
%
% Begin FTM bibliography style
%
\DeclareSourcemap{%
	\maps{%
		\map[overwrite=true]{%
			\step[fieldsource=doi, match={\regexp{\{\\textunderscore.*\}}}, replace={_}]%
		}%
		\map[overwrite=true]{%
			\step[fieldsource=urldate,%
			match=\regexp{([0-9]{2})\.([0-9]{2})\.([0-9]{4})},%
			replace={$3-$2-$1},%$
			final]%
		}%
		\map[overwrite=true]{%
			\step[fieldsource=date,%
			match=\regexp{([0-9]{2})\.([0-9]{2})\.([0-9]{4})},%
			replace={$3-$2-$1},%$
			final]%
		}%
		\map[overwrite]{
			\step[fieldsource=titleaddon, final]
			\step[fieldset=titleaddon, fieldvalue={~}, append]
		}
		\map[overwrite=true]{%
			\step[fieldsource=keywords,%
			match=\regexp{(me.*inPress|inPress.*me)}, final]%
			\step[fieldset=titleaddon, fieldvalue={(in press)}, append]%
		}%
		\map[overwrite=true]{%
			\step[fieldsource=keywords,%
			match=\regexp{(me.*accepted|accepted.*me)}, final]%
			\step[fieldset=titleaddon, fieldvalue={(accepted)}, append]%
		}%
		\map[overwrite=true]{%
			\step[fieldsource=keywords,%
			match=\regexp{(me.*inReview|inReview.*me)}, final]%
			\step[fieldset=titleaddon, fieldvalue={(in review process)}, append]%
		}%
	}%
}%
%
% Declare cite as category and nocite without numbers
\DeclareBibliographyCategory{cited}%
\AtEveryCitekey{\addtocategory{cited}{\thefield{entrykey}}}%
\defbibenvironment{bibliographyNoReference}%
{\list%
  {\ifcategory{cited}{\printtext[labelnumberwidth]{%
		\printfield{labelprefix}%
		\printfield{labelnumber}}}{}}%
  {\setlength{\labelwidth}{\labelnumberwidth}%
	\setlength{\leftmargin}{\labelwidth}%
	\setlength{\labelsep}{\biblabelsep}%
	\addtolength{\leftmargin}{\labelsep}%
	\setlength{\itemsep}{\bibitemsep}%
	\setlength{\parsep}{\bibparsep}%
	\ifcategory{cited}{\renewcommand*{\makelabel}[1]{\hss##1}}{}}}%
{\endlist}%
{\item}%
%
% Declare general bibliography styles
% German Firstinitial. Last
\DeclareNameAlias{default}{first-last}
% two authors with last, first., three authors with et al.
\PassOptionsToPackage{bibstyle=ieee}{biblatex}%
\ExecuteBibliographyOptions{minnames=1, mincrossrefs=1, datezeros=true}
% Three or more authors first author + et al.
\DefineBibliographyStrings{ngerman}{andothers={et\ al\adddot}}% Use german et.al.
% Last author with and/und
\renewcommand*{\finalnamedelim}{\space\FTMlangLiteratureAndName\space}%
% Declar that dots are no full stops
\DeclareFieldFormat[norm,patent,article,online,thesis,report,book,inproceedings,incollection,collection,notice]{title}{\mkbibemph{#1\isdot}}%
\DeclareFieldFormat{number}{\mkbibemph{#1}\isdot}
% Title not italic for all exept book and collection, number not italic for norm, patent, report
\DeclareFieldFormat[norm,patent,article,online,thesis,report,inproceedings,incollection,notice]{title}{{#1}}%
\DeclareFieldFormat[norm,patent,report]{number}{{#1}}%
% Declare how to print urls
\DeclareFieldFormat{url}{\bibstring{available}\addcolon\space\url{#1}}
\DeclareFieldFormat{urldate}{[{\bibstring{urlseen}\space#1}]}
% Inherit data from crossreferences (book -> incollection: title, editor, series, publisher, address, year) (proceedings -> inproceedings: venue, title)
\DeclareDataInheritance{proceedings}{inproceedings}{\inherit{venue}{venue}\inherit{title}{booktitle}}%
\DeclareDataInheritance{book}{incollection}{\inherit{address}{address}\inherit{title}{booktitle}\inherit{editor}{editor}\inherit{series}{series}\inherit{publisher}{publisher}\inherit{year}{year}}%
% Controll spelling
\NewBibliographyString{available}
\DefineBibliographyStrings{english}{available = {Available}}%
\DefineBibliographyStrings{german}{available = {Verfügbar}}%
\DefineBibliographyStrings{english}{urlseen = {visited on}}%
\DefineBibliographyStrings{german}{urlseen = {aufgerufen am}}%
% Declare bibmacros
\renewbibmacro{title}{\printtext{\glqq}\printfield{title}\printtext{\addcomma}\printtext{\grqq}\setunit*{\space}\printfield{titleaddon}}
\newbibmacro{titleIEEE}{\printtext{\glqq}\printfield{title}\printtext{\addcomma}\printtext{\grqq}\setunit*{\space}\printfield{titleaddon}}%
\newbibmacro{titleIEEE+booktitle}{\usebibmacro{titleIEEE}\setunit*{\addcomma\space}\iffieldundef{booktitle}{}{\printtext{in\addspace\textit{\thefield{booktitle}}}}}%
\newbibmacro{day+month+year}{%
  \iffieldundef{day}{}{\printtext{\mkdayzeros{\thefield{day}}}\setunit{\FTMlangLiteratureOnlineDateSeperator}}%
  \iffieldundef{month}{}{\printtext{\mkmonthzeros{\thefield{month}}}\setunit*{\FTMlangLiteratureOnlineDateSeperator}}%
  \iffieldundef{year}{}{\printfield{year}}}%
\newbibmacro{volume}{\iffieldundef{volume}{}{\printtext{\FTMlangLiteratureVolumeName\addspace\thefield{volume}}}}%
\newbibmacro{number}{\iffieldundef{number}{}{\printtext{\FTMlangLiteratureNumberName\addspace\thefield{number}}}}%
\newbibmacro{repository}{\iffieldundef{number}{}{\printtext{\addspace\FTMlangLiteratureRepositoryName\addspace}\printfield{number}}}
\newbibmacro{series}{\iffieldundef{series}{}{\printtext{(\thefield{series})}}}%
%% Declare category article
\DeclareBibliographyDriver{norm}{%
\printfield{title}%
\setunit*{\addcomma\space}%
\printfield{type}%
\setunit*{\space}%
\printfield{number}%
\setunit*{\addcomma\space}%
\printfield{year}%
\finentry}%
\DeclareBibliographyDriver{patent}{%
\printnames{author}%
\setunit*{\addcomma\space}%
\usebibmacro{titleIEEE}%
\setunit*{\space}%
\printlist{location}%
\setunit*{\space}%
\printtext{Patent}%
\setunit*{\space}%
\printfield{number}%
\setunit{\addcomma\addspace}
\iffieldundef{month}{}{\printtext{\FTMlangMonth{\thefield{month}}}}%
\setunit*{\nobreakspace}%
\printtext{\mkdayzeros{\thefield{day}}}%
\setunit*{\addcomma\nobreakspace}
\printfield{year}
\finentry}%
\DeclareBibliographyDriver{article}{%
\printnames{author}%
\setunit*{\addcomma\space}%
\usebibmacro{titleIEEE}%
\setunit*{\addcomma\space}%
\usebibmacro{journal}%
\setunit*{\addcomma\space}%
\usebibmacro{volume}%
\setunit*{\addcomma\space}%
\usebibmacro{number}
\setunit*{\addcomma\space}%
\printfield{pages}%
\setunit*{\addcomma\space}%
\printfield{year}%
\setunit*{\addcomma\space}%
\printfield{isbn}%
\setunit*{\adddot\space}%
\usebibmacro{doi+eprint+url}%
\finentry}%
%\ifdefined\optEnglish%
\DeclareBibliographyDriver{online}{%
\printnames{author}%
\setunit*{\adddot\space}%
\usebibmacro{titleIEEE}%
\setunit*{\addcomma\space}%
\printfield{urlyear}
\setunit*{\adddot\space}%
\printtext{[Online]}%
\setunit*{\adddot\space}%
\usebibmacro{url+urldate}%
\finentry}%
\DeclareBibliographyDriver{thesis}{%
\printnames{author}%
\setunit*{\addcomma\space}%
\usebibmacro{titleIEEE}%
\setunit*{\addcomma\space}%
\printfield{type}%
\setunit*{\addcomma\space}%
\printlist{publisher}%
\setunit*{\addcomma\space}%
\printlist{institution}%
\setunit*{\addcomma\addspace}
\printlist{location}%
\setunit*{\addcomma\addspace}%
\printfield{year}%
\setunit*{\addcomma\space}%
\printfield{isbn}%
\setunit*{\adddot\space}%
\usebibmacro{doi+eprint+url}%
\finentry}%
\DeclareBibliographyDriver{report}{%
\printnames{author}%
\setunit*{\addcomma\space}%
\usebibmacro{titleIEEE}%
\setunit*{\addcomma\space}%
\printlist{institution}%
\setunit*{\addcomma\space}%
\printlist{location}%
\usebibmacro{repository}%
\setunit{\addcomma\addspace}
\printfield{pages}%
\setunit*{\addcomma\space}%
\usebibmacro{day+month+year}
\setunit*{\addcomma\space}%
\printfield{isbn}%
\setunit*{\adddot\space}%
\usebibmacro{doi+eprint+url}%
\finentry}%
\DeclareBibliographyDriver{book}{%
\printnames{author}%
\setunit*{\addcomma\space}%
\printfield{title}%
\setunit*{\addcomma\space}%
\usebibmacro{series}%
\setunit*{\adddot\space}%
\usebibmacro{volume}%
\setunit*{\addcomma\space}%
\printfield{edition}%
\setunit*{\addcomma\space}%
\printlist{location}%
\setunit*{\addcomma\space}%
\printlist{publisher}%
\setunit*{\addcomma\space}%
\printfield{pages}%
\setunit*{\addcomma\space}%
\printfield{year}%
\setunit*{\addcomma\space}%
\printfield{isbn}%
\setunit*{\adddot\space}%
\usebibmacro{doi+eprint+url}%
\finentry}%
\DeclareBibliographyDriver{inproceedings}{%
\printnames{author}%
\setunit*{\addcomma\space}%
\usebibmacro{titleIEEE+booktitle}%
\setunit*{\addcomma\space}%
\iffieldundef{venue}{}{\printfield{venue}}%
\setunit*{\addcomma\space}%
\printfield{year}%
\setunit*{\addcomma\space}%
\printfield{pages}%
\setunit*{\addcomma\space}%
\printfield{isbn}%
\setunit*{\adddot\space}%
\usebibmacro{doi+eprint+url}%
\finentry}%
\DeclareBibliographyDriver{incollection}{%
\printnames{author}%
\setunit*{\addcomma\space}%
\usebibmacro{titleIEEE+booktitle}%
\setunit*{\space}%
\usebibmacro{series}%
\setunit*{\adddot\space}%
\usebibmacro{volume}
\setunit*{\addcomma\space}%
\ifnameundef{editor}{}%
  {\printnames{editor}\addcomma\space\printtext{\FTMlangLiteratureEditorName}}%
\setunit*{\space}%
\printlist{location}
\setunit*{\addcolon\space}%
\printlist{publisher}
\setunit*{\addcomma\space}%
\printfield{year}%
\setunit*{\addcomma\space}%
\printfield{pages}%
\setunit*{\addcomma\space}%
\printfield{isbn}%
\setunit*{\adddot\space}%
\usebibmacro{doi+eprint+url}%
\finentry}%
\DeclareBibliographyDriver{collection}{%
\printnames{editor}%
\setunit*{\addcomma\space}%
\printfield{title}%
\setunit*{\addcomma\space}%
\usebibmacro{series}
\setunit*{\adddot\space}%
\usebibmacro{volume}%
\setunit*{\addcomma\space}%
\printlist{location}%
\setunit*{\addcomma\space}%
\printlist{publisher}%
\setunit*{\addcomma\space}%
\printfield{pages}%
\setunit*{\addcomma\space}%
\printfield{year}%
\setunit*{\addcomma\space}%
\printfield{isbn}%
\setunit*{\adddot\space}%
\usebibmacro{doi+eprint+url}%
\finentry}%
\DeclareBibliographyDriver{notice}{%
\printnames{author}%
\setunit*{\addcomma\space}%
\usebibmacro{titleIEEE}%
\setunit*{\addcomma\space}%
\printfield{type}%
\setunit*{\addcomma\space}%
\usebibmacro{day+month+year}
\finentry}%
% Do not write URL over margin
\usepackage{url}
\setcounter{biburlnumpenalty}{1000}
\setcounter{biburlucpenalty}{1000}
\setcounter{biburllcpenalty}{1000}
%
% End FTM bibliography style
%
\else\fi% End-check if module FTMbiblio is enabled
%###################################################################################################
%--- END MODULE FTMbiblio --------------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- BEGIN MODULE FTMnames -------------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMnames% Start-check if module FTMnames is enabled
%
% >>> CONTENTS OF FILE source/TUM/Modules/TUMnames.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%==================
%--- Professors ---
%==================
% President
% ---------
\def\FTMnamesProfHerrmann{Prof.\ Dr.\ Dr.\ h.c.\ mult.\ Wolfgang A. Herrmann}%
%
% Active professors
% -----------------
\def\FTMnamesProfAdams{Prof.\ Dr.-Ing.\ Nikolaus A. Adams}%
\def\FTMnamesProfBengler{Prof.\ Dr.\ phil.\ Klaus Bengler}%
\def\FTMnamesProfBerensmeier{Prof.\ Dr.\ Sonja Berensmeier}%
\def\FTMnamesProfBottasso{Prof.\ Dr.\ Carlo L. Bottasso}%
\def\FTMnamesProfDrechsler{Prof.\ Dr.-Ing.\ Klaus Drechsler}%
\def\FTMnamesProfFottner{Prof.\ Dr.-Ing.\ Johannes Fottner}%
\def\FTMnamesProfGee{Prof.\ Dr.-Ing.\ Michael W. Gee}%
\def\FTMnamesProfGuemmer{Prof.\ Dr.-Ing.\ Volker Gümmer}%
\def\FTMnamesProfGuenthner{Prof.\ Dr.-Ing.\ Willibald A. Günthner}%
\def\FTMnamesProfHaidn{Prof.\ Dr.-Ing.\ Oskar J. Haidn}%
\def\FTMnamesProfHajek{Prof.\ Dr.-Ing.\ Manfred Hajek}%
\def\FTMnamesProfHolzapfel{Prof.\ Dr.-Ing.\ Florian Holzapfel}%
\def\FTMnamesProfHornung{Prof.\ Dr.-Ing.\ Mirko Hornung}%
\def\FTMnamesProfKaltenbach{Prof.\ Dr.-Ing.\ Hans-Jakob Kaltenbach}%
\def\FTMnamesProfKlein{Prof.\ Dr.-Ing.\ Harald Klein}%
\def\FTMnamesProfKoutsourelakis{Prof.\ Ph.D.\ Phaedon-Stelios Koutsourelakis}%
\def\FTMnamesProfKremling{Prof.\ Dr.-Ing.\ Andreas Kremling}%
\def\FTMnamesProfLieleg{Prof.\ Dr.\ Oliver Lieleg}%
\def\FTMnamesProfLienkamp{Prof.\ Dr.-Ing.\ Markus Lienkamp}%
\def\FTMnamesProfLindemann{Prof.\ Dr.-Ing.\ Udo Lindemann}%
\def\FTMnamesProfLohmann{Prof.\ Dr.-Ing.\ Boris Lohmann}%
\def\FTMnamesProfLueth{Prof.\ Dr.\ rer.\ nat.\ Tim C. Lüth}%
\def\FTMnamesProfMacianJuan{Prof.\ Dr.\ Rafael Macián-Juan}%
\def\FTMnamesProfMarburg{Prof.\ Dr.-Ing.\ Steffen Marburg}%
\def\FTMnamesProfNeu{Prof.\ Dr.\ rer.\ nat.\ Rudolf Neu}%
\def\FTMnamesProfPolifke{Prof.\ Dr.\ Wolfgang Polifke}%
\def\FTMnamesProfProvost{Prof.\ Dr.\ Julien Provost}%
\def\FTMnamesProfReinhart{Prof.\ Dr.-Ing.\ Gunther Reinhart}%
\def\FTMnamesProfRixen{Prof.\ dr.ir.\ Daniel J. Rixen}%
\def\FTMnamesProfSattelmayer{Prof.\ Dr.-Ing.\ Thomas F. Sattelmayer}%
\def\FTMnamesProfSenner{Prof.\ Dr.-Ing.\ Veit Senner}%
\def\FTMnamesProfSpannerUlmer{Prof.\ Dr.\ Birgit Spanner-Ulmer}%
\def\FTMnamesProfSpliethoff{Prof.\ Dr.-Ing.\ Hartmut Spliethoff}%
\def\FTMnamesProfStahl{Prof.\ Dr.-Ing.\ Karsten Stahl}%
\def\FTMnamesProfVogelHeuser{Prof.\ Dr.-Ing.\ Birgit Vogel-Heuser}%
\def\FTMnamesProfVolk{Prof.\ Dr.-Ing.\ Wolfram Volk}%
\def\FTMnamesProfWachtmeister{Prof.\ Dr.\ Georg Wachtmeister}%
\def\FTMnamesProfWall{Prof.\ Dr.-Ing.\ Wolfgang A. Wall}%
\def\FTMnamesProfWalter{Prof.\ Dr.\ Ulrich Walter}%
\def\FTMnamesProfWerner{Prof.\ Dr.\ Ewald Werner}%
\def\FTMnamesProfWeusterBotz{Prof.\ Dr.-Ing.\ Dirk Weuster-Botz}%
\def\FTMnamesProfZaeh{Prof.\ Dr.-Ing.\ Michael Zäh}%
%
%
% >>> CONTENTS OF FILE source/FTM/Modules/FTMnames.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%
%
% Scientific Employees
% --------------------
\def\FTMnamesStaffBetz{Johannes Betz, M.Sc.}%
\def\FTMnamesStaffBuechner{Stefan Büchner, M. Sc.}%
\def\FTMnamesStaffEisele{Andreas Eisele, M.Sc.}%
\def\FTMnamesStaffEnders{Erik Enders, M. Sc.}%
\def\FTMnamesStaffFoerth{Matthias Förth, M.Sc.}%
\def\FTMnamesStaffHeilmeier{Alexander Heilmeier, M.Sc.}%
\def\FTMnamesStaffHermansdorfer{Leonhard Hermansdorfer, M.Sc.}%
\def\FTMnamesStaffNobis{Felix Nobis, M.Sc.}%
\def\FTMnamesStaffRiedl{Konstantin Riedl, M. Sc.}%
\def\FTMnamesStaffSchmidt{Michael Schmidt, M.Sc.}%
\def\FTMnamesStaffWagner{Daniel Wagner, M.Sc.}%
\def\FTMnamesStaffZehelein{Thomas Zehelein, M. Sc.}%
\def\FTMnamesStaffWittmann{Michael Wittmann, M. Sc.}%
\def\FTMnamesStaffAdenaw{Lennart Adenaw, M.Sc.}%
\def\FTMnamesStaffKloeppel{Dipl.-Ing. Manfred Klöppel}%
\def\FTMnamesStaffKreibich{Julian Kreibich, M. Sc.}%
\def\FTMnamesStaffMerkle{Lukas Merkle, M. Sc.}%
\def\FTMnamesStaffSchmid{Werner Schmid, M.Sc.}%
\def\FTMnamesStaffWaclaw{Adam Waclaw, M. Sc.}%
\def\FTMnamesStaffDiermeyer{Dr.-Ing. Frank Diermeyer}%
\def\FTMnamesStaffFank{Jana Fank, M.Sc.}%
\def\FTMnamesStaffFeiler{Johannes Feiler, M.Sc.}%
\def\FTMnamesStaffGeorg{Jean-Michael Georg, M.Sc.}%
\def\FTMnamesStaffHauenstein{Jürgen Hauenstein, M.Sc.}%
\def\FTMnamesStaffHoffmann{Simon Hoffmann, M.Sc.}%
\def\FTMnamesStaffKnies{Christian Knies, M.Sc.}%
\def\FTMnamesStaffMertens{Jan Cedric Mertens, M.Sc.}%
\def\FTMnamesStaffPonn{Thomas Ponn, M.Sc.}%
\def\FTMnamesStaffRichardson{Natalie Richardson, M.Sc.}%
\def\FTMnamesStaffSchatz{Julian Schatz, M.Sc.}%
\def\FTMnamesStaffStahl{Tim Stahl, M.Sc.}%
\def\FTMnamesStaffAngerer{Christian Angerer, M.Sc.}%
\def\FTMnamesStaffBroenner{Matthias Brönner, M.Sc.}%
\def\FTMnamesStaffDanquah{Benedikt Danquah, M.Sc.}%
\def\FTMnamesStaffFelgenhauer{Matthias Felgenhauer, M.Sc.}%
\def\FTMnamesStaffKoberstaedt{Dipl.-Ing. Sascha Koberstaedt}%
\def\FTMnamesStaffKrapf{Sebastian Krapf, M.Sc.}%
\def\FTMnamesStaffKoch{Alexander Koch, M.Sc.}%
\def\FTMnamesStaffKoenig{Adrian König, M.Sc.}%
\def\FTMnamesStaffPathak{Aditya Pathak, M.Sc.}%
\def\FTMnamesStaffSchockenhoff{Ferdinand Schockenhoff, M.Sc.}%
\def\FTMnamesStaffSethuraman{Ganesh Sethuraman, M.Sc.}%
\def\FTMnamesStaffSoltes{Dipl.-Ing. Martin Soltes}%
\def\FTMnamesStaffWolff{Sebastian Wolff, M.Sc.}%
\def\FTMnamesStaffReiter{Christoph Reiter, M.Sc.}%
\def\FTMnamesStaffAdermann{Jörn Adermann, M.Sc.}%
\def\FTMnamesStaffBaumann{Dipl.-Ing. Michael Baumann}%
\def\FTMnamesStaffChang{Fengqi Chang, M. Sc.}%
\def\FTMnamesStaffFabian{Dipl.-Phys. Fabian Ebert}%
\def\FTMnamesStaffGewald{Tanja Gewald, M.Sc.}%
\def\FTMnamesStaffKalt{Svenja Kalt, M.Sc.}%
\def\FTMnamesStaffLin{Xue Lin, M.Sc.}%
\def\FTMnamesStaffMinnerup{Katharina Minnerup, M. Sc.}%
\def\FTMnamesStaffRohr{Stephan Rohr, M.Sc.}%
\def\FTMnamesStaffRoemer{Dipl.-Ing. Felix Römer}%
\def\FTMnamesStaffSteinstraeter{Matthias Steinsträter, M.Sc.}%
\def\FTMnamesStaffWassiliadis{Nikolaos Wassiliadis, M.Sc.}%
\def\FTMnamesStaffWildfeuer{Leo Wildfeuer, M.Sc.}%
%
%
%
\else\fi% End-check if module FTMnames is enabled
%###################################################################################################
%--- END MODULE FTMnames ---------------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- BEGIN MODULE FTMutils -------------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMutils% Start-check if module FTMutils is enabled
%
% >>> CONTENTS OF FILE source/TUM/Modules/TUMutils.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%================
%--- Packages ---
%================
\RequirePackage{excludeonly}%              Provides command to exclude source files (for editing large documents)
\RequirePackage{epstopdf}%                 Automatically converts .eps files to .pdf
\RequirePackage{xspace}%                   Provides command to insert/skip whitespace after a command
\RequirePackage{cancel}%                   Provides commands to strike through text and math expressions
\RequirePackage{datetime}%                 Provides current date and time
\RequirePackage{eurosym}%                  Provides the euro symbol
\RequirePackage{blindtext}%                Helper to write blind text for templates
\ifdefined\optFTMbeamer\else%              Avoid clash with beamer baseclass
	\RequirePackage[clearempty]{titlesec}% Customize captions etc. (has to be leaded BEFORE hyperref)
	\RequirePackage{titletoc}%             Customize table of contents (has to be leaded BEFORE hyperref)
	\RequirePackage{pdfcomment}%           Allows PDF-comments and PDF-annotations (loads package hyperref -> should be the last package!)
\fi%
%
%
%================
%--- Commands ---
%================
\DeclareExpandableDocumentCommand{\FTMutilsTodo}{O{red}m}{%
	\ifdefined\optHideTodos\else%
		{\texorpdfstring{\color{#1}\textbf{ToDo:} #2}{}}%
	\fi%
}%
\DeclareExpandableDocumentCommand{\FTMutilsTodoW}{O{red}m}{%
	\ifdefined\optHideTodos\else%
		\FTMutilsTodo[#1]{#2}\FTMcoreLogWarning{#2}%
	\fi%
}%
\newcommand{\FTMutilsTodoSpacer}[2][]%
{%
	\ifdefined\optHideTodos\else%
		\ifx\\#1\\% check, if first argument is not empty
			\ \\[-0.5\baselineskip]%
		\else%
			\ \\{\color{red}\footnotesize ToDo: #1}\ \\[-0.8\baselineskip]%
		\fi%
		\tikz \draw[red,line width=0.5mm] (0cm,0cm) -- (\textwidth-1.4pt,0cm);%
		\FTMcoreRepetition{#2}{\\[-\baselineskip]\vspace{1mm}\ \\[-\baselineskip]\tikz \draw[red,line width=0.5mm] (0cm,0cm) -- (0cm,1mm); \hfill \tikz \draw[red,line width=0.5mm] (0cm,0cm) -- (0cm,1mm);}%
		\\[-\baselineskip]\tikz \draw[red,line width=0.5mm] (0cm,0cm) -- (\textwidth-1.4pt,0cm);\\%
	\fi%
}%
%
% PDF comments, annotations and highlights
% ----------------------------------------
\DeclareExpandableDocumentCommand{\FTMutilsPDFanno}{O{unknown}m}{%
	\ifdefined\optHideAnnotations\else%
		\texorpdfstring{\pdfcomment[icon=Note,color=yellow,opacity=0.5,author={#1}]{#2}}{}%
	\fi%
}%
\DeclareExpandableDocumentCommand{\FTMutilsPDFannoColor}{O{unknown}mm}{%
	\ifdefined\optHideAnnotations\else%
		\texorpdfstring{\pdfcomment[icon=Note,color=#3,opacity=0.5,author={#1}]{#2}}{}%
	\fi%
}%
\DeclareExpandableDocumentCommand{\FTMutilsPDFhigh}{O{yellow}m}{%
	\ifdefined\optHideAnnotations\else%
		\texorpdfstring{\pdfmarkupcomment[markup=Highlight,color=#1]{#2}{}}{}%
	\fi%
}%
%
% Date and time
% -------------
\newcommand{\FTMutilsDate}[3]{\FTMlangGerEng{#1. \FTMlangMonth{#2} #3}{\FTMlangMonth{#2} #1, #3}}
%
\newcommand{\FTMutilsToday}{\FTMutilsDate{\the\day}{\the\month}{\the\year}}
%
%
% >>> CONTENTS OF FILE source/FTM/Modules/FTMutils.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%
%
%%
%
%
% Begin FTM listings
\RequirePackage{listings}% 					% Load Package for Listings
\RequirePackage[numbered]{./source/packages/mcode}% 	% Code-Highlighting, Options: frame, autolinebreaks,
\RequirePackage{textcomp}%					% Don't know
\lstset{literate=
	{á}{{\'a}}1 {é}{{\'e}}1 {í}{{\'i}}1 {ó}{{\'o}}1 {ú}{{\'u}}1
	{Á}{{\'A}}1 {É}{{\'E}}1 {Í}{{\'I}}1 {Ó}{{\'O}}1 {Ú}{{\'U}}1
	{à}{{\`a}}1 {è}{{\`e}}1 {ì}{{\`i}}1 {ò}{{\`o}}1 {ù}{{\`u}}1
	{À}{{\`A}}1 {È}{{\'E}}1 {Ì}{{\`I}}1 {Ò}{{\`O}}1 {Ù}{{\`U}}1
	{ä}{{\"a}}1 {ë}{{\"e}}1 {ï}{{\"i}}1 {ö}{{\"o}}1 {ü}{{\"u}}1
	{Ä}{{\"A}}1 {Ë}{{\"E}}1 {Ï}{{\"I}}1 {Ö}{{\"O}}1 {Ü}{{\"U}}1
	{â}{{\^a}}1 {ê}{{\^e}}1 {î}{{\^i}}1 {ô}{{\^o}}1 {û}{{\^u}}1
	{Â}{{\^A}}1 {Ê}{{\^E}}1 {Î}{{\^I}}1 {Ô}{{\^O}}1 {Û}{{\^U}}1
	{œ}{{\oe}}1 {Œ}{{\OE}}1 {æ}{{\ae}}1 {Æ}{{\AE}}1 {ß}{{\ss}}1
	{ű}{{\H{u}}}1 {Ű}{{\H{U}}}1 {ő}{{\H{o}}}1 {Ő}{{\H{O}}}1
	{ç}{{\c c}}1 {Ç}{{\c C}}1 {ø}{{\o}}1 {å}{{\r a}}1 {Å}{{\r A}}1
	{€}{{\euro}}1 {£}{{\pounds}}1 {«}{{\guillemotleft}}1
	{»}{{\guillemotright}}1 {ñ}{{\~n}}1 {Ñ}{{\~N}}1 {¿}{{?`}}1
	{~}{{\textasciitilde}}1}%
% Declare listing options
\definecolor{CodeNumberGrey}{RGB}{127,127,127}% Grau für Zeilennummern
\lstset{aboveskip=12pt, belowskip=12pt, abovecaptionskip=\smallskipamount, belowcaptionskip=\smallskipamount, xleftmargin=0.08\textwidth, xrightmargin=0.05\textwidth, numbers=left, numberstyle=\color{CodeNumberGrey}, stepnumber=1, breaklines=true, breakatwhitespace=false, breakautoindent=true, basicstyle=\ttfamily\footnotesize, showspaces=false, showstringspaces=false, showtabs=false, keepspaces=true, frame=none}
%
%
%% Eigenen Style für eine Programmiersprache definieren, damit Schriftart, -größe und Abstände angepasst werden können und ausschließlich SQL-Code formatiert wird:
\definecolor{SQLBlue}{RGB}{0,0,127}% Blau, wie es von pgAdmin3 für Keywords verwendet wird.
\definecolor{SQLGreen}{RGB}{0,127,0}% Gruen, wie es von pgAdmin3 für Kommentare verwendet wird.
\definecolor{SQLPurple}{RGB}{127,0,127}% Violett, wie es von pgAdmin3 für Strings verwendet wird.
\lstdefinestyle{SQLStyleFTM}{language=FTMsql,
	keywordstyle=\color{SQLBlue}\ttfamily,
	stringstyle=\color{SQLPurple}\ttfamily,
	commentstyle=\color{SQLGreen}\ttfamily,
}
\definecolor{PythonPurple}{RGB}{153,0,153}
\definecolor{PythonGreen}{RGB}{0,153,0}
\lstdefinestyle{PythonStyleFTM}{language=FTMpython,
	keywordstyle=\color{orange},
	keywordstyle={[2]\color{PythonPurple}},
	stringstyle=\color{PythonGreen},
	commentstyle=\color{red},
	%upquote=true,                      % requires textcomp
}%
\lstdefinestyle{JavaStyleFTM}{language=FTMjava,
	keywordstyle=\color{orange},
	keywordstyle={[2]\color{PythonPurple}},
	stringstyle=\color{PythonGreen},
	commentstyle=\color{red},
}%
\lstdefinestyle{CStyleFTM}{language=FTMc,
	keywordstyle=\color{orange},
	keywordstyle={[2]\color{PythonPurple}},
	stringstyle=\color{PythonGreen},
	commentstyle=\color{red},
}%
\lstdefinestyle{CppStyleFTM}{language=FTMcpp,
	keywordstyle=\color{orange},
	keywordstyle={[2]\color{PythonPurple}},
	stringstyle=\color{PythonGreen},
	commentstyle=\color{red},
}%
% End FTM listings
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%
%
%
%
% Begin FTM instruction
\newcommand{\FTMinstruction}[2]{\\[12pt]\begin{minipage}[c]{\linewidth}\centering\fcolorbox{black}{TUMGray3}{\parbox{0.8\textwidth}{\textbf{#1}\newline #2}}\end{minipage}\\[12pt]}%
% End FTM instruction
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Begin FTM ToDo
% TODO-Package (dieses arbeitet mit Tikz):
\ifdefined\optHideTodos%
	\PassOptionsToPackage{disable}{todonotes}%
\fi%
\RequirePackage[%
colorinlistoftodos,
textsize=scriptsize		% als Schriftgröße einfach die Latex-Schrfitgröße angeben
]{todonotes}				% Einbinden von Todonotes zum Vermerken von noch offenen ToDos im Dokument
\setlength{\marginparwidth}{1.9cm} % erlaubte Breite der Sprechblasen, muss an Seitenrand angepasst werden.
\makeatletter \renewcommand{\todo}[2][]{\tikzexternaldisable\@todo[#1]{#2}\tikzexternalenable} \makeatother
%
% End FTM ToDo
%
%
%
\else\fi% End-check if module FTMutils is enabled
%###################################################################################################
%--- END MODULE FTMutils ---------------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- BEGIN MODULE FTMref ---------------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMref% Start-check if module FTMref is enabled
%
% >>> CONTENTS OF FILE source/TUM/Modules/TUMref.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%================
%--- Packages ---
%================
\RequirePackage{hyperref}%
\hypersetup{%
	%bookmarks=true,%
	linkcolor=TUMBlue,%
	citecolor=TUMBlue,%
	urlcolor=TUMBlue,%
	colorlinks=true}%
\ifdefined\optFTMbeamer\else%              Avoid clash with beamer baseclass
	\ifdefined\optGerman%
		\PassOptionsToPackage{ngerman}{cleveref}%
	\else\fi%
	\ifdefined\optEnglish%
		\PassOptionsToPackage{english}{cleveref}%
	\else\fi%
	\RequirePackage{cleveref}%
\fi%
%
%================
%--- Commands ---
%================
% Set PDF meta data
\newcommand{\FTMrefSetPDFMetadata}[6]{%
	\hypersetup{pdftitle={#1},pdfsubject={#2},pdfauthor={#3},pdfkeywords={#4},pdfcreator={#5},pdfproducer={#6}}%
}%
%
%
%========================
%--- Execute defaults ---
%========================
\FTMrefSetPDFMetadata{}{}{}{}{TUMlatex project}{}%
\urlstyle{same}%
%
%
% >>> CONTENTS OF FILE source/FTM/Modules/FTMref.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\ifdefined\optFTMstudentthesis
	\hypersetup{%
		bookmarksnumbered = true}%
\else
	\ifdefined\optFTMphdthesis
		\hypersetup{%
			bookmarksnumbered = true}%
\fi\fi
%
% Begin FTM autoref options
\addto\extrasngerman{%
	\def\chapterautorefname{Kapitel}%
	\def\sectionautorefname{Unterkapitel}%
	\def\subsectionautorefname{Abschnitt}%
	\def\subsubsectionautorefname{Unterabschnitt}%
	\def\figureautorefname{Abbildung}%
	\def\tableautorefname{Tabelle}%
	\def\listingautorefname{Code}%
  \def\appendixautorefname{Anhang}
}%
%
\addto\captionsngerman{%
	\renewcommand{\figurename}{Abbildung}%
	\renewcommand{\tablename}{Tabelle}%
	\renewcommand{\listfigurename}{Abbildungsverzeichnis}%
	\renewcommand{\lstlistingname}{Code}%
}%
%

\addto\extrasenglish{%
	\def\chapterautorefname{Chapter}%
	\def\sectionautorefname{Section}%
	\def\subsectionautorefname{Subsection}%
	\def\subsubsectionautorefname{Subsubsection}%
	\def\figureautorefname{Figure}%
	\def\tableautorefname{Table}%
	\def\listingautorefname{Listing}%
  \def\appendixautorefname{Appendix}%
}%
%
\addto\captionsenglish{%
	\renewcommand{\figurename}{Figure}%
	\renewcommand{\tablename}{Table}%
	\renewcommand{\lstlistingname}{Listing}%
}%
%
% End FTM autoref options
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Begin FTM referencing
\RequirePackage{nameref}
%
\def\FTMcontentsName{\FTMlangGerEng{Inhaltsverzeichnis}{Contents}}%
\def\FTMappendixName{\FTMlangGerEng{Anhang}{Appendix}}%
\def\FTMglossaryName{\FTMlangGerEng{Abkürzungsverzeichnis}{List of Abbreviations}}%
\def\FTMformulaSymbolsName{\FTMlangGerEng{Formelzeichen}{Formula Symbols}}%
\def\FTMformulaSymbolsUnitName{\FTMlangGerEng{Einheit}{Unit}}%
\def\FTMformulaSymbolsDescriptionName{\FTMlangGerEng{Beschreibung}{Description}}%
\def\FTMliteratureName{\FTMlangGerEng{Literaturverzeichnis}{Bibliography}}%
\def\FTMrefandName{\FTMlangGerEng{und}{and}}%
\def\FTMrefeqnandName{\FTMlangGerEng{Gleichung}{Equation}}%
%
\newcommand*{\FTMfullref}[1]{\hyperref[{#1}]{\autoref*{#1}~\nameref*{#1}}}%	% reference section with full name
%
\newcommand*{\FTMsecref}[1]{\autoref{#1}}%									% reference section
%
\newcommand*{\FTMsectworef}[2]{\autoref{#1}~\FTMrefandName~\ref{#2}}%		% reference 2 sections
%
\newcommand*{\FTMfigref}[1]{\autoref{#1}}%									% reference figure
%
\newcommand*{\FTMfigtworef}[2]{\autoref{#1}~\FTMrefandName~\ref{#2}}%		% reference 2 figures
%
\newcommand*{\FTMfigtoref}[2]{\autoref{#1}\,-\,\ref{#2}}%					% reference multiple figures
%
\newcommand*{\FTMeqnref}[1]{\FTMrefeqnandName~(\ref{#1})}%									% reference equation
%
\newcommand*{\FTMeqntworef}[2]{\FTMrefeqnandName~(\ref{#1})~\FTMrefandName~(\ref{#2})}%		% reference 2 equations
%
\newcommand*{\FTMeqntoref}[2]{\FTMrefeqnandName~(\ref{#1})\,-\,(\ref{#2})}% 					% reference multiple equations
%
\newcommand*{\FTMtabref}[1]{\autoref{#1}}%									% reference table
%
\newcommand*{\FTMtabtworef}[2]{\autoref{#1}~\FTMrefandName~\ref{#2}}% 		% reference 2 tables
%
\newcommand*{\FTMtabtoref}[2]{\autoref{#1}\,-\,\ref{#2}}% 					% reference multiple tables
%
\newcommand*{\FTMlstref}[1]{\autoref{#1}}%									% reference listing
%
\newcommand*{\FTMlsttworef}[2]{\autoref{#1}~\FTMrefandName~\ref{#2}}% 		% reference 2 listings
%
\newcommand*{\FTMlsttoref}[2]{\autoref{#1}\,-\,\ref{#2}}% 					% reference multiple listings
%
% End FTM referencing
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%
\else\fi% End-check if module FTMref is enabled
%###################################################################################################
%--- END MODULE FTMref -----------------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- BEGIN STYLE FTMdocumentation ------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMdocumentation% Start-check if style FTMdocumentation is enabled
%
% >>> CONTENTS OF FILE source/TUM/Styles/TUMdocumentation.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%================
%--- Packages ---
%================
\RequirePackage{caption}%
\RequirePackage{longtable}%
\RequirePackage{fancyhdr}%
%
%
%=============
%--- Style ---
%=============
% Set default layout
\geometry{left=2.5cm,right=3cm,top=2.5cm,bottom=3cm,headsep=1cm,headheight=14pt}%
%
% Paragraph indentation
\parindent0pt%
\parskip0.5em%
%
% Package titlesec: chapter and section style
\titlespacing\chapter{0pt}{20pt plus 4pt minus 2pt}{10pt plus 2pt minus 2pt}%
\titlespacing\section{0pt}{15pt plus 4pt minus 2pt}{7pt plus 2pt minus 2pt}%
\titlespacing\subsection{0pt}{10pt plus 2pt minus 2pt}{2pt plus 2pt minus 2pt}%
\titlespacing\subsubsection{0pt}{10pt plus 2pt minus 2pt}{2pt plus 2pt minus 2pt}%
\titleformat{\chapter}[display]{\color{TUMBlue}\sffamily\huge\bfseries}{\chaptertitlename\ \thechapter}{1em}{}%
\titleformat{\section}{\color{TUMBlue}\sffamily\Large\bfseries}{\thesection}{1em}{}%
\titleformat{\subsection}{\color{TUMBlue}\sffamily\large\bfseries}{\thesubsection}{1em}{}%
\titleformat{\subsubsection}{\color{TUMBlue}\sffamily\normalsize\bfseries}{\thesubsubsection}{1em}{}%
%
%% Package fancyhdr: header and footer style
\fancypagestyle{FTMdocumentationp}{%
	\AtBeginDocument{%
		\renewcommand{\sectionmark}[1]{\markright{\thesection\ \ ##1}}%
		\renewcommand{\chaptermark}[1]{\markboth{\thechapter\ \ ##1}{}}%
	}%
	\fancyhf{}%
	\fancyhead[R]{\normalcolor\normalsize\bfseries\sffamily\thepage}%
	\fancyhead[L]{\normalcolor\normalsize\itshape\sffamily\nouppercase{\rightmark}}%
	\renewcommand{\headrulewidth}{0pt}%
	\renewcommand{\footrulewidth}{0pt}%
}%
%
% Set pagestyle for mainmatter
\pagestyle{FTMdocumentationp}%
%
% First page of chapter empty instead of plain style
\patchcmd{\chapter}{plain}{empty}{}{}%
%
% Hyperref style
\hypersetup{linkcolor=TUMBlue,urlcolor=TUMBlue}%
%
% Caption style
\captionsetup{labelfont=bf,font={sf,small}}%
%
%
%================
%--- Commands ---
%================
\newcommand{\FTMdocumentationModule}[1]{\texttt{\color{TUMGreen}#1}}%
\newcommand{\FTMdocumentationStyle}[1]{\texttt{\color{TUMOrange}#1}}%
\newcommand{\FTMdocumentationTemplate}[1]{\texttt{\color{TUMGray2}#1}}%
\newcommand{\FTMdocumentationOption}[1]{\texttt{\color{TUMGray2}#1}}%
\newcommand{\FTMdocumentationCode}[1]{\texttt{#1}}%
%
%
% >>> CONTENTS OF FILE source/FTM/Styles/FTMdocumentation.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%
%
%
\else\fi% End-check if style FTMdocumentation is enabled
%###################################################################################################
%--- END STYLE FTMdocumentation --------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- BEGIN STYLE FTMphdthesis ----------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMphdthesis% Start-check if style FTMphdthesis is enabled
%
% >>> CONTENTS OF FILE source/TUM/Styles/TUMphdthesis.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%=================
%--- Titlepage ---
%=================
% Titlepage (TUM corporate design)
% ---------
\newcommand{\FTMphdthesisTitlePage}[8]{{%
	\thispagestyle{empty}%
	\newgeometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}%
	\FTMlayoutPutAtNorthWest{2.5cm}{1.5cm}{\FTMlogoDepartment{1cm}{TUMBlue}}%
	\FTMlayoutPutAtNorthEast{1.5cm}{1.5cm}{\FTMlogoTUM{1cm}{TUMBlue}}%
	\sffamily%
	\vskip1.4cm%
	\Large \FTMlangForceGerman{\FTMlangDepartment}\\\FTMlangForceGerman{\FTMlangChair}\par%
	% Title
	\vskip2cm%
	\huge\textbf{#1}\par%
	% Subtitle
	\textit{#2}%
	\vskip1cm%
	% Author
	\textcolor{TUMBlack}{\bfseries\fontsize{13pt}{18pt}\selectfont #3}\par%
	\vskip1cm%
	%
	\normalsize
	Vollständiger Abdruck der von der Fakultät für Maschinenwesen der Technischen Universität München zur Erlangung des akademischen Grades eines\par\vskip1em%
	\textbf{Doktor-Ingenieurs (Dr.-Ing.)}\par\vskip1em%
	genehmigten Dissertation.\par%
	\vfill%
	\textbf{Vorsitzender:} #4\par%
	\vskip1em%
	\textbf{Prüfer der Dissertation:}\par\vskip0.3em 1. #5\par\vskip0.3em 2. #6\par%
	\vskip1.5cm%
	Die Dissertation wurde am \FTMlangForceGerman{#7} bei der Technischen Universität München eingereicht und durch die Fakultät für Maschinenwesen am \FTMlangForceGerman{#8} angenommen.%
	\vskip2cm%
	\cleardoublepage%
	\restoregeometry%
}}%
%
%
% >>> CONTENTS OF FILE source/FTM/Styles/FTMphdthesis.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%================
%--- Packages ---
%================
\RequirePackage{caption}%
\RequirePackage{fancyhdr}%
\RequirePackage[titles]{tocloft}%
\RequirePackage[nottoc]{tocbibind}%
\RequirePackage{units}%
\RequirePackage[nogroupskip,acronyms,nopostdot,style=super,nonumberlist,toc]{glossaries}%
\RequirePackage{etoc}% load tocloft befor etoc to avoid error
\RequirePackage[all]{nowidow}%
% Acronyms
\setacronymstyle{long-short}%
\ifdefined\optGroupedAbbreviation
  \renewcommand*{\glsgroupskip}{\\[-7pt]}%
\else\fi
\setlength{\glsdescwidth}{0.8\textwidth}%
%
%=============
%--- Style ---
%=============
% Set default layout
\geometry{left=2.5cm,right=2.5cm,top=2.7cm,bottom=2cm,headsep=0.8cm,headheight=20pt,footskip=0.75cm-11pt}%
%
% Paragraph indentation
\newcommand{\FTMMainText}{%
  \cleardoublepage
	\parindent0pt%
	\parskip6pt%
	\pagestyle{FTMphdthesisp}%
	\renewcommand{\sectionmark}[1]{\markright{\thesection\ \ ##1}}%
	\renewcommand{\chaptermark}[1]{\markboth{\thechapter\ \ ##1}{}}%
	\setcounter{page}{1}%
	\pagenumbering{arabic}%
	\cleardoublepage%
  \sisetup{detect-none,mode=math,math-rm=\mathrm}%
}%
%
%
% Paragraph indentation
\newcommand{\FTMPreText}{%
  \frenchspacing%
	\parindent0pt%
	\parskip6pt%
	\setcounter{page}{1}% That's how the Word-Template of FTM is formatted.
	\thispagestyle{empty}% Starting at first page
	\pagestyle{empty}% Pagenumbering even for pages before list of contents.
	\pagenumbering{Alph}
	\cleardoublepage%
	\etocdepthtag.toc{mtchapter}%
	\etocsettagdepth{mtchapter}{subsection}%
	\etocsettagdepth{mtappendix}{none}%
  \sisetup{detect-none,mode=math,math-rm=\mathrm}% use correct typo for SI in text
}%
%
%
\newcommand{\FTMPostText}{%
	\cleardoublepage%
  \parindent0pt%
	\parskip6pt%
	\setcounter{page}{1}% That's how the Word-Template of FTM is formatted.
	\pagestyle{FTMphdthesisp}% Pagenumbering even for pages before list of contents.
	\renewcommand{\sectionmark}[1]{\markright{\thesection\ \ ##1}}%
	\renewcommand{\chaptermark}[1]{\markboth{\thechapter\ \ ##1}{}}%
	\pagenumbering{roman}%
	\cleardoublepage%
  \listoffigures%
	\cleardoublepage%
	\listoftables%
	\cleardoublepage%
  %\markboth{\FTMlangLiteratureName}{\FTMlangLiteratureName}%
}%
%
%
\newcommand{\FTMAppendix}{%
	\cleardoublepage%
  \phantomsection%
  \parindent0pt%
	\parskip6pt%
	\pagestyle{FTMphdthesisp}%
	\cleardoublepage%
	\addcontentsline{toc}{chapter}{\FTMlangAppendixName}%
	\renewcommand{\contentsname}{\FTMlangAppendixName}%
	\renewcommand{\thechapter}{\Alph{chapter}}%
	\renewcommand{\theHchapter}{\appendixname.\thechapter}%
	\etocdepthtag.toc{mtappendix}%
	\etocsettagdepth{mtchapter}{none}%
	\etocsettagdepth{mtappendix}{subsection}%
}%
%
%
% Package titlesec: chapter and section style
\titlespacing\chapter{0pt}{44pt}{33.4pt}%
\titlespacing\section{0pt}{26pt}{9pt}%
\titlespacing\subsection{0pt}{18pt}{0pt}%
\titlespacing\subsubsection{0pt}{18pt}{0pt}%
\titlespacing\paragraph{0pt}{12pt}{0pt}%
\titleformat{\chapter}{\color{TUMBlack}\sffamily\bfseries\fontsize{24pt}{24}\selectfont}{\thechapter}{0.5em}{}%
\titleformat{\section}{\color{TUMBlack}\sffamily\bfseries\fontsize{18pt}{18}\selectfont}{\thesection}{0.8em}{}%
\titleformat{\subsection}{\color{TUMBlack}\sffamily\bfseries\fontsize{14pt}{14}\selectfont}{\thesubsection}{0.8em}{}%
\titleformat{\subsubsection}{\color{TUMBlack}\sffamily\bfseries\fontsize{14pt}{14}\selectfont}{\thesubsubsection}{0.8em}{}%
\titleformat{\paragraph}{\color{TUMBlack}\sffamily\bfseries\fontsize{12pt}{12}\selectfont}{\thesubsubsection}{0.8em}{}%
%
%% Package fancyhdr: header and footer style
\fancypagestyle{FTMphdthesisp}{%
	\fancyhf{}%
	\fancyhead[LE,RO]{\normalcolor\normalsize\sffamily\nouppercase{\leftmark}}%
	\fancyfoot[LE,RO]{\normalcolor\normalsize\sffamily\thepage}%
	\renewcommand{\headrulewidth}{0.5pt}%
	\renewcommand{\headrule}{\vspace{-0.15cm}\hbox to\headwidth{%
			\color{TUMBlack}\leaders\hrule height \headrulewidth\hfill}}%
	\renewcommand{\footrulewidth}{0pt}%
}%
%
%
% Hyperref style (no color)
\hypersetup{linkcolor=black,urlcolor=black, citecolor=black}%
% Create PDF in 2-page-view
\hypersetup{pdfpagelayout=TwoPageRight}
%
%
%=================
%--- Titlepage ---
%=================
%
\newcommand{\FTMphdthesisTitlePageFTMDesign}[8]{{%
		\hypersetup{pageanchor=false}%
		\thispagestyle{empty}%
		\newgeometry{left=2.5cm,right=2.5cm,top=2.7cm,bottom=2cm}%
		\vspace*{0.13cm}%
		% Head
		\centerline{\sffamily\fontsize{18}{18} \selectfont Technische Universität München}\par\vskip13pt%
		\centerline{\sffamily\fontsize{11}{11} \selectfont \FTMlangForceGerman{\FTMlangDepartment}}\par\vskip9pt%
		\centerline{\sffamily\fontsize{11}{11} \selectfont \FTMlangForceGerman{\FTMlangChair}}\par%
		\vspace{3.4cm}\noindent%
		% Title
		\parbox{\textwidth}{\centering\sffamily\fontsize{18}{26.5} \selectfont\textbf{#1}}\par\vskip16pt%
		%
		\centerline{\fontsize{18}{18} \selectfont #3}\par%
		\vspace{3.5cm}%
		% Additional Text
		\parbox{\textwidth}{\centering \sffamily\fontsize{11}{11} \selectfont Vollständiger Abdruck der von der Fakultät für Maschinenwesen der \\[6pt] Technischen Universität München zur Erlangung des akademischen Grades eines}\par\vskip13pt%
		\centerline{\sffamily\fontsize{18}{18} \selectfont Doktor-Ingenieurs}\par\vskip13pt%
		\centerline{\sffamily\fontsize{11}{11} \selectfont genehmigten Dissertation.}\par%
		\vspace{3.3cm}%
		% Committee
		\makebox[6.3cm][l]{Vorsitzender:}#5\par\vskip4pt%
		\makebox[6.3cm][l]{Prüfer der Dissertation:}\makebox[9.7cm][l]{1.~\FTMnamesProfLienkamp}\par\vskip3pt%
		\makebox[6.3cm][l]{}\makebox[9.7cm][l]{2.~#6}\par%
		\vfill%
		\parbox{\textwidth}{\fontsize{11}{16} \selectfont Die Dissertation wurde am \FTMlangForceGerman{#7} bei der Technischen Universität München eingereicht und durch die Fakultät für Maschinenwesen am \FTMlangForceGerman{#8} angenommen.}\par%
		\vspace{0.7cm}%
		\cleardoublepage%
		\restoregeometry%
		\hypersetup{pageanchor=true}%
}}%
%
%=====================================================
%--- Table of contents, List of figures and tables ---
%=====================================================
% Table of contents
\ifdefined\optFTMphdthesis%
\renewcommand{\cftchapfont}{\sffamily\normalsize\bfseries}%
\renewcommand{\cftsecfont}{\sffamily\normalsize\bfseries}%
\renewcommand{\cftsubsecfont}{\sffamily\normalsize}%
\renewcommand{\cftchappagefont}{\sffamily\normalsize\bfseries}
\renewcommand{\cftsecpagefont}{\sffamily\normalsize\bfseries}
\renewcommand{\cftsubsecpagefont}{\sffamily\normalsize}
\renewcommand{\cftchapindent}{0cm}%
\renewcommand{\cftsecindent}{0.39cm}%
\renewcommand{\cftsubsecindent}{0.78cm}%
\setlength{\cftbeforechapskip}{0pt}%
\setlength{\cftbeforesecskip}{0pt}%
\setlength{\cftbeforesubsecskip}{0pt}%
\setlength{\cftchapnumwidth}{0.63cm}%
\setlength{\cftsecnumwidth}{0.88cm}%
\setlength{\cftsubsecnumwidth}{1.12cm}%
\renewcommand{\cftdotsep}{0.5}%
\renewcommand{\cftchapdotsep}{\cftdotsep}%
\renewcommand{\cftsecdotsep}{\cftdotsep}%
\renewcommand{\cftsubsecdotsep}{\cftdotsep}%
\renewcommand{\cftchapdotsep}{\cftdotsep}%
\renewcommand{\cftchapleader}{\cftdotfill{\cftchapdotsep}}%
\setcounter{tocdepth}{2}%
% List of Figures and Tables
\renewcommand{\cftfigaftersnum}{:}%
\renewcommand{\cfttabaftersnum}{:}%
\renewcommand{\cftfigindent}{0cm}%
\renewcommand{\cfttabindent}{0cm}%
\renewcommand\cftfigpresnum{\figurename~}%
\newlength\cftfiglabellength%
\settowidth\cftfiglabellength{\cftfigpresnum}%
\addtolength\cftfignumwidth{3.25cm-\cftfiglabellength}%
\renewcommand\cfttabpresnum{\tablename~}%
\newlength\cfttablabellength%
\settowidth\cfttablabellength{\cfttabpresnum}%
\addtolength\cfttabnumwidth{2.75cm-\cfttablabellength}%
% To remove extra vertical space before chapter in list of figures and tables
\newcommand*{\noaddvspace}{\renewcommand*{\addvspace}[1]{}}
\addtocontents{lof}{\protect\noaddvspace}
\addtocontents{lot}{\protect\noaddvspace}
\else%
\fi%
%
%===================
%--- Frontmatter ---
%===================
\newcommand{\FTMPrintTableOfContents}{%
	\setcounter{page}{1}%
  \pagenumbering{Roman}%
	\markboth{\FTMlangContentsName}{\FTMlangContentsName}%
	\pdfbookmark{\FTMlangContentsName}{\FTMlangContentsName}%
	\tableofcontents%
	\pagestyle{plain}%
	\cleardoublepage%
  \parskip6pt%
	\printnoidxglossary[type=acronym,sort=standard,title={\FTMlangGlossaryName}]%  Print list of Acronyms
}%
%
%
\newcommand{\FTMPrintTableOfAppendix}{%
	\markboth{\FTMlangAppendixName}{\FTMlangAppendixName}%
	\tableofcontents%
	\thispagestyle{plain}%
	\cleardoublepage%
}%
%
%
% Change plain style
\fancypagestyle{plain}{%
	\fancyhf{} % clear all header and footer fields
	\fancyfoot[LE,RO]{\normalcolor\large\sffamily\thepage}%
	\renewcommand{\headrulewidth}{0pt}%
	\renewcommand{\footrulewidth}{0pt}}%
%
%
% Change frontmatter page numbering to uppercase roman
\makeatletter
%
\renewcommand\frontmatter{%
	\cleardoublepage
	%\@mainmatterfalse
	\pagenumbering{Roman}}
%
\makeatother
%
%
%===================
%--- Backmatter ---
%===================
%
\let\origappendix\appendix % save the existing appendix command
\renewcommand{\appendix}{\cleardoublepage\pagenumbering{roman}\origappendix} %
%
%
\else\fi% End-check if style FTMphdthesis is enabled
%###################################################################################################
%--- END STYLE FTMphdthesis ------------------------------------------------------------------------
%###################################################################################################
%
%
%
%
%
%###################################################################################################
%--- BEGIN STYLE FTMstudentthesis ------------------------------------------------------------------
%###################################################################################################
\ifdefined\optFTMstudentthesis% Start-check if style FTMstudentthesis is enabled
%
% >>> CONTENTS OF FILE source/TUM/Styles/TUMstudentthesis.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%=================
%--- Titlepage ---
%=================
% Titlepage (TUM corporate design)
% ---------
\newcommand{\FTMstudentthesisTitlePageCD}[8]{%
	\thispagestyle{empty}%
	% Logo
	\FTMlayoutPutAtNorthEast{2cm}{1.5cm}{\FTMlogoTUM{1cm}{TUMBlue}}%
	\vskip3.5cm\noindent%
	% Title
	\textcolor{TUMBlue}{\sffamily\bfseries\fontsize{24pt}{30pt}\selectfont #1}\par%
	\vskip1em\noindent%
	% Subtitle
	\textcolor{TUMGray3}{\sffamily\bfseries\fontsize{20pt}{30pt}\selectfont #2}\par%
	\vskip2cm\noindent%
	\vfill%
	% Subject
	{\sffamily%
		\fontsize{14pt}{14pt}\selectfont #7\par%
		\fontsize{16pt}{16pt}\selectfont #8\par%
		\fontsize{14pt}{14pt}\selectfont an der Fakultät für Maschinenwesen der Technischen Universität München\par%
	}\par%
	\vskip2cm\noindent%
	% Info
	{\sffamily\fontsize{12pt}{14pt}\selectfont%
		\begin{tabular}{@{}p{0.22\textwidth}p{0.75\textwidth}}%
			\bfseries \FTMlangSupervisedBy & #4 \newline #5\newline\FTMlangChairFTM\\[3em]%
			\bfseries \FTMlangSubmittedBy & #3\\[3em]%
			\bfseries \FTMlangSubmittedOn & \FTMlangForceGerman{#6}\\%
		\end{tabular}%
	}%
	\vskip1cm%
	\cleardoublepage%
	\thispagestyle{empty}%
	% Disclaimer at end of document with thesis date
	\AtEndDocument{%
	\chapter*{\FTMlangGerEng{Erklärung}{Disclaimer}}%
	\FTMlangGerEng{Hiermit erkläre ich, dass ich die vorliegende Arbeit selbständig und ohne Benutzung anderer als der angegebenen Hilfsmittel angefertigt habe. Alle Stellen, die wörtlich oder sinngemäß aus veröffentlichten und nicht veröffentlichten Schriften entnommen sind, sind als solche kenntlich gemacht. Die Arbeit ist in gleicher oder ähnlicher Form -- auch auszugsweise -- noch nicht im Rahmen einer anderen Prüfung vorgelegt worden.}{I hereby declare that this thesis is entirely the result of my own work except where otherwise indicated. I have only used the resources given in the list of references.}%
	\vskip4\baselineskip%
	Garching, #6\hfill $\overline{\makebox[60mm]{\centering\footnotesize(\FTMlangGerEng{Unterschrift}{Signature})}}$%
	}%
}%
\newcommand{\FTMstudentthesisTitlePageCDDiplomarbeit}[6]{%
	\FTMstudentthesisTitlePageCD{#1}{#2}{#3}{#4}{#5}{#6}{Wissenschaftliche Arbeit zur Erlangung des Grades}{Diplom Ingenieur (Dipl.-Ing.)}%
}%
\newcommand{\FTMstudentthesisTitlePageCDBachelorsThesis}[6]{%
	\FTMstudentthesisTitlePageCD{#1}{#2}{#3}{#4}{#5}{#6}{Wissenschaftliche Arbeit zur Erlangung des Grades}{Bachelor of Science (B. Sc.)}%
}
\newcommand{\FTMstudentthesisTitlePageCDSemesterThesis}[6]{%
	\FTMstudentthesisTitlePageCD{#1}{#2}{#3}{#4}{#5}{#6}{}{\FTMlangSemesterThesis}%
}%
\newcommand{\FTMstudentthesisTitlePageCDMasterThesis}[6]{%
	\FTMstudentthesisTitlePageCD{#1}{#2}{#3}{#4}{#5}{#6}{Wissenschaftliche Arbeit zur Erlangung des Grades}{Master of Science (M.Sc.)}%
}%
\newcommand{\FTMstudentthesisTitlePageCDIDP}[6]{%
	\FTMstudentthesisTitlePageCD{#1}{#2}{#3}{#4}{#5}{#6}{}{\FTMlangInterdisciplinaryProject}%
}%
%
%
% >>> CONTENTS OF FILE source/FTM/Styles/FTMstudentthesis.sty: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
%================
%--- Packages ---
%================
\RequirePackage{caption}%
\RequirePackage{fancyhdr}%
\RequirePackage[titles]{tocloft}%
\RequirePackage[nottoc]{tocbibind}%
\RequirePackage{units}%
\RequirePackage[nogroupskip,acronyms,nopostdot,style=super,nonumberlist,toc]{glossaries}%
\RequirePackage{etoc}% load tocloft befor etoc to avoid error
\RequirePackage[all]{nowidow}%
% Acronyms
\setacronymstyle{long-short}%
\ifdefined\optGroupedAbbreviation
  \renewcommand*{\glsgroupskip}{\\[-7pt]}%
\else\fi
\setlength{\glsdescwidth}{0.8\textwidth}%
%
%=============
%--- Style ---
%=============
% Set default layout
\geometry{left=2.5cm,right=2.5cm,top=2.7cm,bottom=2cm,headsep=0.8cm,headheight=25pt,footskip=0.75cm-11pt}%
%
% Paragraph indentation
\newcommand{\FTMMainText}{%
  \cleardoublepage%
	\parindent0pt%
	\parskip6pt%
	\pagestyle{FTMstudentthesisp}%
	\renewcommand{\sectionmark}[1]{\markright{\thesection\ \ ##1}}%
	\renewcommand{\chaptermark}[1]{\markboth{\thechapter\ \ ##1}{}}%
	\setcounter{page}{1}%
	\pagenumbering{arabic}%
	\cleardoublepage%
  \sisetup{detect-none,mode=math,math-rm=\mathrm}%
}%
%
%
% Paragraph indentation
\newcommand{\FTMPreText}{%
  \frenchspacing%
	\parindent0pt%
	\parskip6pt%
	\setcounter{page}{1}% That's how the Word-Template of FTM is formatted.
	\thispagestyle{empty}% Starting at first page
	\pagestyle{empty}% Pagenumbering even for pages before list of contents.
	\pagenumbering{Alph}
	\cleardoublepage%
	\etocdepthtag.toc{mtchapter}%
	\etocsettagdepth{mtchapter}{subsection}%
	\etocsettagdepth{mtappendix}{none}%
  \sisetup{detect-none,mode=math,math-rm=\mathrm}% use correct typo for SI in text
}%
%
%
\newcommand{\FTMPostText}{%
  \cleardoublepage%
  \parindent0pt%
	\parskip6pt%
	\setcounter{page}{1}% That's how the Word-Template of FTM is formatted.
	\pagestyle{FTMstudentthesisp}% Pagenumbering even for pages before list of contents.
	\renewcommand{\sectionmark}[1]{\markright{\thesection\ \ ##1}}%
	\renewcommand{\chaptermark}[1]{\markboth{\thechapter\ \ ##1}{}}%
	\pagenumbering{roman}%
	\cleardoublepage%
	\listoffigures%
	\cleardoublepage%
	\listoftables%
	\cleardoublepage%
  \markboth{\FTMlangLiteratureName}{\FTMlangLiteratureName}%
}%
%
%
\newcommand{\FTMAppendix}{%
  \cleardoublepage%
  \phantomsection%
	\parindent0pt%
	\parskip6pt%
	\pagestyle{FTMstudentthesisp}%
	\cleardoublepage%
	\addcontentsline{toc}{chapter}{\FTMlangAppendixName}%
	\renewcommand{\contentsname}{\FTMlangAppendixName}%
	\renewcommand{\thechapter}{\Alph{chapter}}%
	\renewcommand{\theHchapter}{\appendixname.\thechapter}%
	\etocdepthtag.toc{mtappendix}%
	\etocsettagdepth{mtchapter}{none}%
	\etocsettagdepth{mtappendix}{subsection}%
}%
%
%
% Package titlesec: chapter and section style
\titlespacing\chapter{0pt}{44pt}{33.4pt}%
\titlespacing\section{0pt}{26pt}{9pt}%
\titlespacing\subsection{0pt}{18pt}{0pt}%
\titlespacing\subsubsection{0pt}{18pt}{0pt}%
\titleformat{\chapter}{\color{TUMBlack}\sffamily\bfseries\fontsize{24pt}{24}\selectfont}{\thechapter}{0.5em}{}%
\titleformat{\section}{\color{TUMBlack}\sffamily\bfseries\fontsize{18pt}{18}\selectfont}{\thesection}{0.8em}{}%
\titleformat{\subsection}{\color{TUMBlack}\sffamily\bfseries\fontsize{14pt}{14}\selectfont}{\thesubsection}{0.8em}{}%
\titleformat{\subsubsection}{\color{TUMBlack}\sffamily\bfseries\fontsize{14pt}{14}\selectfont}{\thesubsubsection}{0.8em}{}%
%
%% Package fancyhdr: header and footer style
\fancypagestyle{FTMstudentthesisp}{%
	\fancyhf{}%
	\fancyhead[LE,RO]{\normalcolor\normalsize\sffamily\nouppercase{\leftmark}}%
	\fancyfoot[LE,RO]{\normalcolor\normalsize\sffamily\thepage}%
	\renewcommand{\headrulewidth}{0.5pt}%
	\renewcommand{\headrule}{\vspace{-0.15cm}\hbox to\headwidth{%
			\color{TUMBlack}\leaders\hrule height \headrulewidth\hfill}}%
	\renewcommand{\footrulewidth}{0pt}%
}%
%
%
%
% Hyperref style (no color)
\hypersetup{linkcolor=black,urlcolor=black, citecolor=black}%
% Create PDF in 2-page-view
\hypersetup{pdfpagelayout=TwoPageRight}
%
% Caption style
%\captionsetup{labelfont={sf,footnotesize},font={sf,footnotesize}}%
%
%=================
%--- Titlepage ---
%=================
%
% Titlepage (FTM custom design)
% ---------
\newcommand{\FTMstudentthesisTitlePageFTMDesign}[9]{%
	\newgeometry{left=2cm,right=2.1cm,top=3.9cm,bottom=2cm}%
	\hypersetup{pageanchor=false}
	\thispagestyle{empty}%
	% Logo
	\FTMlayoutPutAtNorthEast{2cm}{2cm}{\FTMlogoTUM{1cm}{TUMBlue}}%
	%	%\FTMlayoutPutAtNorthEast{2cm}{1.5cm}{\FTMlogoFTM{1.0cm}{FTMLogoColorBottom}{FTMLogoColorMiddle}{FTMLogoColorTop}}% Test of FTM-Logo
	\vskip0.25cm\noindent%
	% Title
	\parbox{\textwidth}{\sffamily\bfseries\fontsize{24pt}{27pt}\selectfont \textcolor{TUMBlack}{#1}}\par%
	\vskip0.7cm\noindent%
	% Subtitle
	\parbox{\textwidth}{\sffamily\fontsize{18pt}{20pt}\selectfont \textcolor{TUMBlack}{#2}}\par%
	\ifthenelse{\equal {#7} {}}%
	{%
		\vskip2cm\noindent%
	}%
	{%
		\vfill
		\begin{figure}[h]%
			\centering%
			\includegraphics[width=0.9\textwidth,height=7.2cm,keepaspectratio]{#7}%
		\end{figure}%
	}%
	\vfill%
	% Subject
	{\sffamily%
		\noindent\fontsize{14pt}{14pt}\selectfont #8\\[0.65em]%
		\noindent\fontsize{14pt}{14pt}\selectfont #9\\[0.65em]%
		\noindent\fontsize{14pt}{14pt}\selectfont \begin{raggedright}\FTMlangGerEng{an der Fakultät für Maschinenwesen der Technischen Universität München}{at the \FTMlangDepartment{} of \FTMlangTUM{}}\end{raggedright}\par%
	}\par%
	\vskip1.5cm\noindent%
	% Info
	{\sffamily\fontsize{12pt}{14pt}\selectfont%
		\begin{tabular}{@{}p{0.22\textwidth}p{0.75\textwidth}}%
			\bfseries \FTMlangSupervisedBy & #4 \newline #5\newline\FTMlangChairFTM\\[3em]%
			\bfseries \FTMlangSubmittedBy & #3\\[3em]%
			\bfseries \FTMlangSubmittedOn &  \FTMlangGerEng{#6}{#6}\\%
		\end{tabular}%
	}%
	\vskip1cm%
	\cleardoublepage%
	\thispagestyle{empty}%
	\hypersetup{pageanchor=true}
	\restoregeometry
}%
%
%
\newcommand{\FTMstudentthesisTitlePageFTMDesignDiplomarbeit}[7]{%
	\FTMstudentthesisTitlePageFTMDesign{#1}{#2}{#3}{#4}{#5}{#6}{#7}{\FTMlangScientificWorkForObtainingTheAcademicDegree}{Diplom Ingenieur (Dipl.-Ing.)}%
}%
\newcommand{\FTMstudentthesisTitlePageFTMDesignBachelorsThesis}[7]{%
	\FTMstudentthesisTitlePageFTMDesign{#1}{#2}{#3}{#4}{#5}{#6}{#7}{\FTMlangScientificWorkForObtainingTheAcademicDegree}{Bachelor of Science (B. Sc.)}%
}
\newcommand{\FTMstudentthesisTitlePageFTMDesignSemesterThesis}[7]{%
	\FTMstudentthesisTitlePageFTMDesign{#1}{#2}{#3}{#4}{#5}{#6}{#7}{}{\FTMlangSemesterThesis}%
}%
\newcommand{\FTMstudentthesisTitlePageFTMDesignMastersThesis}[7]{%
	\FTMstudentthesisTitlePageFTMDesign{#1}{#2}{#3}{#4}{#5}{#6}{#7}{\FTMlangScientificWorkForObtainingTheAcademicDegree}{Master of Science (M.Sc.)}%
}%
\newcommand{\FTMstudentthesisTitlePageFTMDesignIDP}[7]{%
	\FTMstudentthesisTitlePageFTMDesign{#1}{#2}{#3}{#4}{#5}{#6}{#7}{}{\FTMlangInterdisciplinaryProject}%
}%
%
%=====================================================
%--- NDA, Erklärung and Declaration of Consent
%=====================================================
\newcommand{\FTMstudentthesisForms}[8]{%
 %
 %%%%%%%%%%%%%%
 %   NDA
 %%%%%%%%%%%%%%
	\hypersetup{pageanchor=false}
	\FTMlayoutPutAtNorthWest{2.5cm}{1.5cm}{\FTMlogoTercetChair{1.05cm}}%
	\FTMlayoutPutAtNorthEast{2.4cm}{2cm}{\FTMlogoTUM{1cm}{TUMBlue}}%

	\vspace{0.3cm}%
	{\fontsize{18}{20}\selectfont Geheimhaltungsverpflichtung}%
	\vspace{1.25cm}%

	#1: {\fontsize{14}{16} \selectfont \textbf{#3, #2}}%

	Gegenstand der Geheimhaltungsverpflichtung sind alle mündlichen, schriftlichen und digitalen Informationen und Materialien die der Unterzeichner vom Lehrstuhl oder von Dritten im Rahmen seiner Tätigkeit am Lehrstuhl erhält. Dazu zählen vor allem Daten, Simulationswerkzeuge und Programmcode sowie Informationen zu Projekten, Prototypen und Produkten.

	Der Unterzeichner verpflichtet sich, alle derartigen Informationen und Unterlagen, die ihm
	während seiner Tätigkeit am Lehrstuhl für Fahrzeugtechnik zugänglich werden, strikt vertraulich
	zu behandeln.

	Er verpflichtet sich insbesondere:%

	\parbox{\textwidth}{\fontsize{11pt}{11pt}\selectfont
		\begin{itemize}[itemsep=\dimexpr -2pt, topsep=0pt, parsep=\dimexpr 5pt, rightmargin=\dimexpr 0cm]
			\item derartige Informationen betriebsintern zum Zwecke der Diskussion nur dann zu verwenden, wenn ein ihm erteilter Auftrag dies erfordert,
			\item keine derartigen Informationen ohne die vorherige schriftliche Zustimmung des Betreuers an Dritte weiterzuleiten,
			\item ohne Zustimmung eines Mitarbeiters keine Fotografien, Zeichnungen oder sonstige Darstellungen von Prototypen oder technischen Unterlagen hierzu anzufertigen,
			\item auf Anforderung des Lehrstuhls für Fahrzeugtechnik oder unaufgefordert spätestens bei seinem Ausscheiden aus dem Lehrstuhl für Fahrzeugtechnik alle Dokumente und Datenträger, die derartige Informationen enthalten, an den Lehrstuhl für Fahrzeugtechnik zurückzugeben.
		\end{itemize}}\vskip6pt

		Eine besondere Sorgfalt gilt im Umgang mit digitalen Daten:%

		\parbox{\textwidth}{\fontsize{11pt}{11pt}\selectfont
			\begin{itemize}[itemsep=\dimexpr -2pt, topsep=0pt, parsep=\dimexpr 5pt, rightmargin=\dimexpr 0cm]
				\item Für den Dateiaustausch dürfen keine Dienste verwendet werden, bei denen die Daten über einen Server im Ausland geleitet oder gespeichert werden (Es dürfen nur Dienste des LRZ genutzt werden (Lehrstuhllaufwerke, Sync\&Share, GigaMove).
				\item Vertrauliche Informationen dürfen nur in verschlüsselter Form per E-Mail versendet werden.
				\item Nachrichten des geschäftlichen E-Mail Kontos, die vertrauliche Informationen enthalten, dürfen nicht an einen externen E-Mail Anbieter weitergeleitet werden.
				\item Die Kommunikation sollte nach Möglichkeit über die (my)TUM-Mailadresse erfolgen.
			\end{itemize}}\vskip6pt

			Die Verpflichtung zur Geheimhaltung endet nicht mit dem Ausscheiden aus dem Lehrstuhl für Fahrzeugtechnik, sondern bleibt 5 Jahre nach dem Zeitpunkt des Ausscheidens in vollem Umfang bestehen. Die eingereichte schriftliche Ausarbeitung darf der Unterzeichner nach Bekanntgabe der Note frei veröffentlichen.%

			Der Unterzeichner willigt ein, dass die Inhalte seiner Studienarbeit in darauf aufbauenden Studienarbeiten und Dissertationen mit der nötigen Kennzeichnung verwendet werden dürfen.%
			%\vspace{0.5cm}%

			Datum: \FTMlangForceGerman{#4}%
			\vspace{0.6cm}%

			Unterschrift: \rule{4.8cm}{1pt}%

			\cleardoublepage%
	\hypersetup{pageanchor=true}
 %
 %%%%%%%%%%%%%%
 %   Erklärung
 %%%%%%%%%%%%%%
	\hypersetup{pageanchor=false}
	\FTMlayoutPutAtNorthWest{2.5cm}{1.5cm}{\FTMlogoTercetChair{1.05cm}}%
	\FTMlayoutPutAtNorthEast{2.4cm}{2cm}{\FTMlogoTUM{1cm}{TUMBlue}}%

	\vspace{0.3cm}%
	{\fontsize{18}{20}\selectfont Erklärung}%
	\vspace{1.1cm}%

	\parbox{\textwidth}{\fontsize{11pt}{15pt}\selectfont Ich versichere hiermit, dass ich die von mir eingereichte Abschlussarbeit selbstständig verfasst und keine anderen als die angegebenen Quellen und Hilfsmittel benutzt habe.}
	\vspace{0.6cm}

	Garching, den \FTMlangForceGerman{#4}
	\vspace{1.4cm}

	\rule{4.8cm}{1pt}
	\vskip0.1cm
	#2 #3#8

	\cleardoublepage
	\hypersetup{pageanchor=true}
 %
 %%%%%%%%%%%%%%
 %    Declaration of Consent
 %%%%%%%%%%%%%%
	\hypersetup{pageanchor=false}
	\FTMlayoutPutAtNorthWest{2.5cm}{1.5cm}{\FTMlogoTercetChair{1.05cm}}%
	\FTMlayoutPutAtNorthEast{2.4cm}{2cm}{\FTMlogoTUM{1cm}{TUMBlue}}%

	\vspace{0.3cm}%
	{\fontsize{18}{20}\selectfont Declaration of Consent, Open Source}%
	\vspace{1.1cm}%

	\parbox{\textwidth}{\fontsize{11pt}{15pt}\selectfont Hereby I, #3, #2, born on \FTMlangForceEnglish{#5}\nospace, make the software I developed during my #6 Thesis available to the Institute of Automotive Technology under the terms of the license below.}
	\vspace{0.6cm}

	Garching, \FTMlangForceEnglish{#4}
	\vspace{1.4cm}

	\rule{4.8cm}{1pt}
	\vskip0.1cm
	#2 #3#8

	\vspace{1.4cm}
	\parbox{\textwidth}{\fontsize{11pt}{15pt}\selectfont Copyright #7 #3, #2}

	\vspace{0.7cm}
	\parbox{\textwidth}{\fontsize{11pt}{15pt}\selectfont Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ``Software''), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.}

	\vspace{0.1cm}
	\parbox{\textwidth}{\fontsize{11pt}{15pt}\selectfont THE SOFTWARE IS PROVIDED ``AS IS'', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MER\-CHANTABIL\-I\-TY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.}

	\cleardoublepage
	\hypersetup{pageanchor=true}
 %
}%
%
%=====================================================
%--- Table of contents, List of figures and tables ---
%=====================================================
% Table of contents
\renewcommand{\cftchapfont}{\sffamily\normalsize\bfseries}%
\renewcommand{\cftsecfont}{\sffamily\normalsize\bfseries}%
\renewcommand{\cftsubsecfont}{\sffamily\normalsize}%
\renewcommand{\cftchappagefont}{\sffamily\normalsize\bfseries}%
\renewcommand{\cftsecpagefont}{\sffamily\normalsize\bfseries}%
\renewcommand{\cftsubsecpagefont}{\sffamily\normalsize} %
\renewcommand{\cftchapindent}{0cm}%
\renewcommand{\cftsecindent}{0.39cm}%
\renewcommand{\cftsubsecindent}{0.78cm}%
\setlength{\cftbeforechapskip}{0pt}%
\setlength{\cftbeforesecskip}{0pt}%
\setlength{\cftbeforesubsecskip}{0pt}%
%\setlength{\cftbeforechapskip}{5pt}%
\setlength{\cftchapnumwidth}{0.63cm}%
\setlength{\cftsecnumwidth}{0.88cm}%
\setlength{\cftsubsecnumwidth}{1.12cm}%
\renewcommand{\cftdotsep}{0.5}%
\renewcommand{\cftchapdotsep}{\cftdotsep}%
\renewcommand{\cftsecdotsep}{\cftdotsep}%
\renewcommand{\cftsubsecdotsep}{\cftdotsep}%
\renewcommand{\cftchapdotsep}{\cftdotsep}%
\renewcommand{\cftchapleader}{\cftdotfill{\cftchapdotsep}}%
\setcounter{tocdepth}{2}%
% List of Figures and Tables
\renewcommand{\cftfigaftersnum}{:}%
\renewcommand{\cfttabaftersnum}{:}%
\renewcommand{\cftfigindent}{0cm}%
\renewcommand{\cfttabindent}{0cm}%
\renewcommand\cftfigpresnum{\figurename~}%
\newlength\cftfiglabellength%
\settowidth\cftfiglabellength{\cftfigpresnum}%
\addtolength\cftfignumwidth{3.25cm-\cftfiglabellength}%
\renewcommand\cfttabpresnum{\tablename~}%
\newlength\cfttablabellength%
\settowidth\cfttablabellength{\cfttabpresnum}%
\addtolength\cfttabnumwidth{2.75cm-\cfttablabellength}%
% To remove extra vertical space before chapter in list of figures and tables
\newcommand*{\noaddvspace}{\renewcommand*{\addvspace}[1]{}}
\addtocontents{lof}{\protect\noaddvspace}
\addtocontents{lot}{\protect\noaddvspace}
%
%===================
%--- Frontmatter ---
%===================
\newcommand{\FTMPrintTableOfContents}{%
	\setcounter{page}{1}%
  \pagenumbering{Roman}%
	\markboth{\FTMlangContentsName}{\FTMlangContentsName}%
	\pdfbookmark{\FTMlangContentsName}{\FTMlangContentsName}%
	\tableofcontents%
	\pagestyle{plain}%
	\cleardoublepage%
  \parskip6pt%
	\printnoidxglossary[type=acronym,sort=standard,title={\FTMlangGlossaryName}]%  Print list of Acronyms
}%
%
%
\newcommand{\FTMPrintTableOfAppendix}{%
	\markboth{\FTMlangAppendixName}{\FTMlangAppendixName}%
	\tableofcontents%
	\thispagestyle{plain}%
	\cleardoublepage%
}%
%
%
% Change plain style
\fancypagestyle{plain}{%
	\fancyhf{} % clear all header and footer fields
	\fancyfoot[LE,RO]{\normalcolor\large\sffamily\thepage}%
	\renewcommand{\headrulewidth}{0pt}%
	\renewcommand{\footrulewidth}{0pt}}%
%
%
% Change frontmatter page numbering to uppercase roman
\makeatletter
%
\renewcommand\frontmatter{%
	\cleardoublepage
	%\@mainmatterfalse
	\pagenumbering{Roman}}
%
\makeatother
%
%
%===================
%--- Backmatter ---
%===================
%
\let\origappendix\appendix % save the existing appendix command
\renewcommand{\appendix}{\cleardoublepage\pagenumbering{roman}\origappendix} %
%
%
%
\else\fi% End-check if style FTMstudentthesis is enabled
%###################################################################################################
%--- END STYLE FTMstudentthesis --------------------------------------------------------------------
%###################################################################################################
%
%
%###################################################################################################
%--- UPDATING --------------------------------------------------------------------------------------
%###################################################################################################
\ifnum\year>2028%
	\def\AMlatexUpdateRecommended{x}%
\else%
	\ifnum\year=2028%
		\ifnum\month>7%
			\def\AMlatexUpdateRecommended{x}%
		\else%
			\ifnum\month=7%
				\ifnum\day>5%
					\def\AMlatexUpdateRecommended{x}%
				\else%
					\ifnum\day=5%
						\def\AMlatexUpdateRecommended{x}%%
					\fi%
				\fi%
			\fi%
		\fi%
	\fi%
\fi%
\ifdefined\AMlatexUpdateRecommended%
	\AMcoreLogWarning{The FTMlatex package you are using is more than ten years old. Please consider an update! Ponn, 2019-08-28}%
\fi%
%
%
%###################################################################################################
%--- DEBUGGING -------------------------------------------------------------------------------------
%###################################################################################################
\newcommand{\FTMlatexPrintOptions}{%
\newpage%
\noindent\textbf{Loaded modules:}\\%
FTMcore: \ifdefined\optFTMcore yes\else no\fi\\%
FTMfont: \ifdefined\optFTMfont yes\else no\fi\\%
FTMlang: \ifdefined\optFTMlang yes\else no\fi\\%
FTMcolor: \ifdefined\optFTMcolor yes\else no\fi\\%
FTMtikz: \ifdefined\optFTMtikz yes\else no\fi\\%
FTMlogo: \ifdefined\optFTMlogo yes\else no\fi\\%
FTMmath: \ifdefined\optFTMmath yes\else no\fi\\%
FTMlayout: \ifdefined\optFTMlayout yes\else no\fi\\%
FTMbiblio: \ifdefined\optFTMbiblio yes\else no\fi\\%
FTMnames: \ifdefined\optFTMnames yes\else no\fi\\%
FTMutils: \ifdefined\optFTMutils yes\else no\fi\\%
FTMref: \ifdefined\optFTMref yes\else no\fi\\%
\noindent\textbf{Loaded substyles:}\\%
FTMbeamer: \ifdefined\optFTMbeamer yes\else no\fi\\%
FTMdocument: \ifdefined\optFTMdocument yes\else no\fi\\%
FTMdocumentation: \ifdefined\optFTMdocumentation yes\else no\fi\\%
FTMempty: \ifdefined\optFTMempty yes\else no\fi\\%
FTMphdexpose: \ifdefined\optFTMphdexpose yes\else no\fi\\%
FTMphdthesis: \ifdefined\optFTMphdthesis yes\else no\fi\\%
FTMposter: \ifdefined\optFTMposter yes\else no\fi\\%
FTMstudentthesis: \ifdefined\optFTMstudentthesis yes\else no\fi\\%
\noindent\textbf{Selected options:}\\%
optHelvetica: \ifdefined\optHelvetica yes\else no\fi\\%
optArial: \ifdefined\optArial yes\else no\fi\\%
optCharter: \ifdefined\optCharter yes\else no\fi\\%
optComputerModern: \ifdefined\optComputerModern yes\else no\fi\\%
optCharterMath: \ifdefined\optCharterMath yes\else no\fi\\%
optComputerModernMath: \ifdefined\optComputerModernMath yes\else no\fi\\%
optGerman: \ifdefined\optGerman yes\else no\fi\\%
optEnglish: \ifdefined\optEnglish yes\else no\fi\\%
optRGB: \ifdefined\optRGB yes\else no\fi\\%
optCMYK: \ifdefined\optCMYK yes\else no\fi\\%
optGray: \ifdefined\optGray yes\else no\fi\\%
optMonochrome: \ifdefined\optMonochrome yes\else no\fi\\%
optTikzExternalize: \ifdefined\optTikzExternalize yes\else no\fi\\%
optLeftEquations: \ifdefined\optLeftEquations yes\else no\fi\\%
optCenterEquations: \ifdefined\optCenterEquations yes\else no\fi\\%
optAfour: \ifdefined\optAfour yes\else no\fi\\%
optAzero: \ifdefined\optAzero yes\else no\fi\\%
optBeamerClassicFormat: \ifdefined\optBeamerClassicFormat yes\else no\fi\\%
optBeamerWideFormat: \ifdefined\optBeamerWideFormat yes\else no\fi\\%
optExzellenz: \ifdefined\optExzellenz yes\else no\fi\\%
optBiber: \ifdefined\optBiber yes\else no\fi\\%
optBibtex: \ifdefined\optBibtex yes\else no\fi\\%
optBibstyleNumeric: \ifdefined\optBibstyleNumeric yes\else no\fi\\%
optBibstyleAlphabetic: \ifdefined\optBibstyleAlphabetic yes\else no\fi\\%
optBibstyleAuthorYear: \ifdefined\optBibstyleAuthorYear yes\else no\fi\\%
optHideTodos: \ifdefined\optHideTodos yes\else no\fi\\%
optHideAnnotations: \ifdefined\optHideAnnotations yes\else no\fi\\%
optGroupedAbbreviation: \ifdefined\optGroupedAbbreviation yes\else no\fi\\%
}%
%
%
\endinput%
