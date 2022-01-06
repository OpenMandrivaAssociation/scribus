%global optflags %{optflags} -Wno-register

Summary:	Scribus - Open Source Page Layout
Name:		scribus
Version:	1.5.7.24797
Release:	1
License:	GPLv2+
Group:		Office
Url:		http://www.scribus.net/
# svn co svn://scribus.net/trunk/Scribus
# cd Scribus
# REV=$(svn info |grep '^Last Changed Rev' |cut -d: -f2- |xargs echo)
# svn export . /tmp/scribus-1.5.7.$REV
# cd /tmp
# tar cJf scribus-1.5.7.$REV.tar.xz scribus-1.5.7.$REV
Source0:	https://downloads.sourceforge.net/project/scribus/scribus-devel/%{version}/scribus-%{version}.tar.xz
Source10:	scribus.rpmlintrc
Patch0:		scribus-1.5.6.1-compile.patch
Patch1:		scribus-1.5.7-zlib-ng-buildfix.patch
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
BuildRequires:	pkgconfig(libfreehand-0.1)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libmspub-0.1)
BuildRequires:	pkgconfig(libpagemaker-0.0)
BuildRequires:	pkgconfig(librevenge-0.0)
BuildRequires:	pkgconfig(libvisio-0.1)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(openscenegraph)
BuildRequires:	pkgconfig(poppler)
BuildRequires:	pkgconfig(poppler-cpp)
BuildRequires:	pkgconfig(poppler-qt5)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	boost-devel
BuildRequires:	cups-devel
BuildRequires:	hyphen-devel
BuildRequires:	jpeg-devel
BuildRequires:	podofo-devel
BuildRequires:  qt5-assistant
BuildRequires:  qt5-designer
BuildRequires:  qt5-linguist
BuildRequires:  qt5-linguist-tools
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(Qt5WebKit)
BuildRequires:	pkgconfig(Qt5WebKitWidgets)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5PrintSupport)

Requires:	ghostscript-common
# Scripter crashes on startup if python isn't there
Requires:	python
# Currently used in font sampler plugin and calendar plugin
Recommends:	tkinter

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
%{_iconsdir}/hicolor/*/apps/%{name}.png
%doc %{_datadir}/doc/%{name}*

#--------------------------------------------------------------------

%package devel
Summary:	Development headers for programs that will use Scribus
Group:		Development/C++

%description devel
Development headers for programs that will use Scribus.

%files devel
%{_includedir}/%{name}

#--------------------------------------------------------------------

%prep
%autosetup -p1
# We don't need NaziOS crap... And it contains python scripts
# that 2to3 will choke on
rm -rf OSX-package

# Don't add (Development) to name in program menu, it makes no sense for
# users
sed -i -e "s/ (Development)//" scribus.desktop.in

%build
%cmake_qt5 -DWANT_HUNSPELL:BOOL=ON -DWANT_HEADERINSTALL:BOOL=ON -DWANT_CPP17:BOOL=ON -G Ninja
%ninja_build

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

# install icons for hicolor and old WM
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -resize 16x16 resources/iconsets/1_5_0/scribus.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert -resize 32x32 resources/iconsets/1_5_0/scribus.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -resize 48x48 resources/iconsets/1_5_0/scribus.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# we do not need KDE stuff
rm -f %{buildroot}%{_datadir}/mimelnk/application/vnd.scribus.desktop
