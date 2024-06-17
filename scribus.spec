%global optflags %{optflags} -Wno-register

Summary:	Scribus - Open Source Page Layout
Name:		scribus
Version:	1.6.2
Release:	1
License:	GPLv2+
Group:		Office
Url:		https://www.scribus.net/
# When packaging a snapshot (sadly, scribus is caught in "release never"):
# svn co svn://scribus.net/trunk/Scribus
# cd Scribus
# REV=$(svn info |grep '^Last Changed Rev' |cut -d: -f2- |xargs echo)
# svn export . /tmp/scribus-1.5.8.$REV
# cd /tmp
# tar cJf scribus-1.5.8.$REV.tar.xz scribus-1.5.8.$REV
Source0:	https://downloads.sourceforge.net/project/scribus/scribus/%{version}/scribus-%{version}.tar.xz
Source10:	scribus.rpmlintrc
#Patch0:		scribus-1.5.8.25628-compile.patch
Patch1:		scribus-1.5.7-zlib-ng-buildfix.patch
# FIXME This is currently too big (essentially pulling the Qt6 fixes from 1.7,
# but also pulling some unrelated bits and pieces)
Patch2:		scribus-qt6.patch
Patch3:		scribus-1.6.1-poppler-24.03.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(harfbuzz)
BuildRequires:	pkgconfig(harfbuzz-icu)
BuildRequires:	pkgconfig(hunspell)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libcdr-0.1)
BuildRequires:	pkgconfig(libzmf-0.0)
BuildRequires:	pkgconfig(libqxp-0.0)
BuildRequires:	pkgconfig(libfreehand-0.1)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libmspub-0.1)
BuildRequires:	pkgconfig(libpagemaker-0.0)
BuildRequires:	pkgconfig(librevenge-0.0)
BuildRequires:	pkgconfig(libvisio-0.1)
BuildRequires:	pkgconfig(xcb-xkb)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(openscenegraph)
BuildRequires:	pkgconfig(poppler)
BuildRequires:	pkgconfig(poppler-cpp)
BuildRequires:	pkgconfig(poppler-qt6)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	boost-devel
BuildRequires:	cups-devel
BuildRequires:	hyphen-devel
BuildRequires:	jpeg-devel
BuildRequires:	podofo-devel
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6WebEngineWidgets)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6Core5Compat)
BuildRequires:	cmake(Qt6OpenGLWidgets)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	qt6-qttools-linguist-tools

Requires:	ghostscript-common
# Scripter crashes on startup if python isn't there
Requires:	python
# Currently used in font sampler plugin and calendar plugin
Recommends:	tkinter

# Nothing outside of scribus uses the headers (and the corresponding
# libraries aren't installed anyway)
Obsoletes:	%{name}-devel < %{EVRD}

%description
Scribus is a desktop open source page layout program with the aim of
producing commercial grade output in PDF and Postscript, primarily,
though not exclusively, for Linux.

While the goals of the program are ease of use and simple
easy-to-understand tools, Scribus offers support for professional
publishing features, such as CMYK colors, easy PDF creation,
Encapsulated Postscript import and export, and creation of color
separations.

%files
%{_bindir}/*
%{_datadir}/%{name}
%{_libdir}/%{name}
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%lang(de) %{_mandir}/de/man1/*
%{_datadir}/applications/*.desktop
%{_datadir}/metainfo/scribus.appdata.xml
%{_datadir}/mime/packages/*.xml
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_datadir}/icons/hicolor/*/mimetypes/application-vnd.scribus.*
%doc %{_datadir}/doc/%{name}*

%prep
%autosetup -p1
# We don't need NaziOS crap... And it contains python scripts
# that 2to3 will choke on
rm -rf OSX-package

# Don't add (Development) to name in program menu, it makes no sense for
# users
sed -i -e "s/ (Development)//" scribus.desktop.in

export PATH=%{_qtdir}/bin:$PATH
%cmake \
	-DWANT_HUNSPELL:BOOL=ON \
	-DWANT_HEADERINSTALL:BOOL=OFF \
	-DWANT_CPP20:BOOL=ON \
	-DWANT_QT6:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

install -d %{buildroot}%{_datadir}/applications
desktop-file-install --vendor='' \
	--dir %{buildroot}%{_datadir}/applications/ \
	--remove-key='Encoding' \
	--remove-category='Graphics' \
	--add-category='Office' \
	--add-category='X-MandrivaLinux-CrossDesktop'\
	%{name}.desktop

# No need to ship headers and static libraries for something not used anywhere else
rm -rf \
	%{buildroot}%{_includedir} \
	%{buildroot}%{_prefix}/lib/*.a \
	%{buildroot}%{_prefix}/lib/cmake

# Or stuff in weird places
rm -rf \
	%{buildroot}%{_prefix}/license
