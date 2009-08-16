%define name    scribus
%define version 1.3.5.1
%define release %mkrel 1

%define	major	0
%define	libname	%mklibname %name %major
%define develname %{name}-devel

Summary: 	Scribus - Open Source Page Layout
Name: 		%name
Version: 	%version
Release:	%release
Source0:	http://downloads.sourceforge.net/project/scribus/scribus-devel/%version/%name-%version.tar.bz2
URL: 		http://www.scribus.net/
License:	GPLv2+
Group:  	Office
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	aspell-devel
BuildRequires:	cups-devel
BuildRequires:	lcms-devel
BuildRequires:	boost-devel
BuildRequires:	cairo-devel
BuildRequires:	qt4-devel >= 3:4.4.0
BuildRequires:	tiff-devel
BuildRequires:	python-devel
BuildRequires:	libtiff-devel
BuildRequires:	desktop-file-utils imagemagick
BuildRequires:	cmake >= 2.6.0
Requires:	tkinter
Requires:	ghostscript-common

Obsoletes:    scribus-i18n-en
Obsoletes:    scribus-i18n-de
Obsoletes:    scribus-i18n-fr
Obsoletes:	%libname

%description
Scribus is a desktop open source page layout program with the aim of
producing commerical grade output in PDF and Postscript, primarily,
though not exclusively, for Linux.

While the goals of the program are ease of use and simple
easy-to-understand tools, Scribus offers support for professional
publishing features, such as CMYK colors, easy PDF creation,
Encapsulated Postscript import and export, and creation of color
separations.

%if %mdkversion < 200900
%post
%update_menus
%update_mime_database
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_mime_database
%clean_icon_cache hicolor
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%lang(de) %{_mandir}/de/man1/*
%{_libdir}/scribus
%{_datadir}/mime/packages/*.xml
%{_datadir}/scribus
%_iconsdir/hicolor/*/apps/%{name}.png
%doc %{_datadir}/doc/%{name}*

#--------------------------------------------------------------------

%package -n	%{develname}
Summary:	Development tools for programs which will use the %libname library
Group:		Development/C++
Obsoletes:	%{libname}-devel
Obsoletes:	libkde3-scribus0-devel
Provides:	libkde3-scribus0-devel

%description -n	%{develname}
The %{develname} package includes the header files and static libraries
necessary for developing programs using the %{libname} library.

If you are going to develop programs which will use this library
you should install %{develname}-devel.  You'll also need to have the %name
package installed.

%files -n %{develname}
%defattr(-,root,root)
%doc AUTHORS COPYING
%_includedir/%name/*

#--------------------------------------------------------------------

%prep
%setup -q
# Don't add (Development) to name in program menu, it makes no sense for
# users
sed -i -e "s/ (Development)//" scribus.desktop

%build
%cmake_qt4
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std -C build

install -d %buildroot%{_datadir}/applications
desktop-file-install --vendor='' \
	--dir %buildroot%{_datadir}/applications/ \
	--remove-key='Encoding' \
	--remove-category='Application' \
	--remove-category='Graphics' \
	--add-category='Office' \
	--add-category='Publishing' \
	--add-category='X-MandrivaLinux-CrossDesktop'\
	%name.desktop

# install icons for hicolor and old WM
mkdir -p %buildroot%_iconsdir/hicolor/{16x16,32x32,48x48}/apps
convert -resize 16x16 scribus/icons/scribus.png %buildroot%_iconsdir/hicolor/16x16/apps/%{name}.png
convert -resize 32x32 scribus/icons/scribus.png %buildroot%_iconsdir/hicolor/32x32/apps/%{name}.png
convert -resize 48x48 scribus/icons/scribus.png %buildroot%_iconsdir/hicolor/48x48/apps/%{name}.png

# we do not need kde stuffs for 2009
rm -f %buildroot%_datadir/mimelnk/application/vnd.scribus.desktop

%clean
rm -rf $RPM_BUILD_ROOT
