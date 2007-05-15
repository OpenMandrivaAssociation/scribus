%define name    scribus
%define version 1.3.3.9
%define rel     1
%define release %mkrel %{rel}

%define	major	0
%define	libname	%mklibname %name %major

# Data should better live in %{_datadir}/scribus/
%define scribusdir %{_libdir}/scribus

Summary: 	Scribus layout program
Name: 		%name
Version: 	%version
Release:	%release
Packager:	Mandriva Linux KDE Team <kde@mandriva.com>
Source0:	http://downloads.sourceforge.net/scribus/scribus-%{version}.tar.bz2
Source1:	%name-i18n-de.tar.bz2
Source2:	%name-i18n-fr.tar.bz2
Source3:	%name-i18n-en.tar.bz2
Source4:	%name-samples-0.1.tar.bz2

URL: 		http://www.scribus.net/

License:	GPL
Group:  	Office
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	autoconf2.5
BuildRequires:	cups-devel
BuildRequires:	lcms-devel
BuildRequires:	libart_lgpl-devel
BuildRequires:	qt3-devel
BuildRequires:	tiff-devel

Requires:	%libname = %version
Obsoletes:	kde3-scribus 
Provides:	kde3-scribus 

%description
Scribus is a DTP (Desktop Publishing) application in the tradtion of
Xpress, Pagemaker or similar. At the moment it is still in the early
stages of development, but fairly usable. You can do all the important
things, such as embedding pictures, placing text on a page and much
more.

Printing is done via the application's own Postscript driver, since the
driver supplied by Qt has too many limitations and each version of it
has its own faults. The driver that ships with Scribus can embed fonts
for printing and can use EPS images at high quality.

At the moment Scribus supports only Type1 (Postscript) and TrueType
fonts.

%package -n	%libname
Summary:	Main libraries for %name
Group:		System/Libraries

Obsoletes:	libkde3-scribus0 
Provides:	libkde3-scribus0 


%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %name.                                                                                                                            

%package -n	%{libname}-devel
Summary:	Development tools for programs which will use the %libname library
Group:		Development/C++
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

Obsoletes:	libkde3-scribus0-devel
Provides:	libkde3-scribus0-devel

%description -n	%{libname}-devel
The %{libname}-devel package includes the header files and static libraries
necessary for developing programs using the %{libname} library.

If you are going to develop programs which will use this library
you should install %{libname}-devel.  You'll also need to have the %name
package installed.

%package -n	%name-i18n-de
Summary:	German documentation for scribus
Group:		Office
Requires:	%name locales-de

%description -n	%name-i18n-de
German documentation for scribus.

%package -n	%name-i18n-fr
Summary:	French documentation for scribus
Group:		Office
Requires:	%name locales-fr

%description -n	%name-i18n-fr
French documentation for scribus.

%prep
%setup -q -a1 -a2 -a3 -a4

%build
export QTDIR=%_prefix/lib/qt3
export KDEDIR=%_prefix

export LD_LIBRARY_PATH=$QTDIR/%{_lib}:$KDEDIR/%{_lib}:$LD_LIBRARY_PATH
export PATH=$QTDIR/bin:$KDEDIR/bin:$PATH
export QTLIB=$QTDIR/%{_lib}

export CFLAGS="$RPM_OPT_FLAGS -I/usr/include/lcms"
export CXXFLAGS="$RPM_OPT_FLAGS -I/usr/include/lcms"

if [ ! -f configure ]; then
	make -f Makefile.cvs
fi

%configure --enable-cairo --disable-debug

#configure i18n
for i in %name-i18n-de %name-i18n-fr %name-i18n-en ; do
	cd $i; ./configure --prefix=/usr; cd ..;
done

#samples
cd %name-samples-0.1
%configure
cd ..

%make

%install
rm -rf $RPM_BUILD_ROOT

# Laurent don't use %%makeinstall it doesn't work
# lib and pugins in not install in good directory.
%makeinstall

install -d -m 0755 %buildroot/%_menudir
cat > %buildroot/%_menudir/%{name} <<EOF
?package(%{name}): \
command="scribus" \
title="Scribus" \
longtitle="Scribus layout program" \
needs="x11" \
section="Applications/Publishing" \
icon="wordprocessor_section.png" \
xdg="true"
EOF

%if %mdkversion > 200600
mkdir $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/scribus.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Scribus
Comment=Scribus layout program
Exec=scribus
Icon=wordprocessor_section.png
Terminal=false
Type=Application
StartupNotify=true
Categories=Qt;KDE;Office;X-KDE-More;X-MandrivaLinux-Office-Publishing;
EOF
%endif

%post
%update_menus

%postun
%clean_menus


%post -n %{libname} -p /sbin/ldconfig                                                                                                        
%postun -n %{libname} -p /sbin/ldconfig                                                                                                      

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README TODO
%_bindir/*
%_menudir/*

%if %mdkversion > 200600
%{_datadir}/applications/scribus.desktop
%endif
%dir %{scribusdir}
%{scribusdir}/*.qm
#%{scribusdir}/*.enc
#%{scribusdir}/*.jpg
%{_datadir}/scribus
%_datadir/mime/packages/scribus.xml
%_libdir//scribus/swatches/*.txt

%{scribusdir}/import.prolog
%{scribusdir}/profiles
%{scribusdir}/dicts

%{_prefix}/lib/scribus/samples
%{scribusdir}/plugins

#%dir %{scribusdir}/icons/
#%{scribusdir}/icons/*.xpm
#%{scribusdir}/icons/*.png
#%{scribusdir}/icons/*.jpg

%_datadir/man/man1/scribus.1*
%_datadir/man/pl/man1/scribus.1*

%{_prefix}/lib/scribus/doc/en
%_libdir/scribus/keysets/scribus13.ksxml
%{_datadir}/pixmaps/*

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING
#%_libdir/%name/libs/*.so*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc AUTHORS COPYING
#%_libdir/%name/libs/*a
%_includedir/%name/*

%files -n %name-i18n-fr
%defattr(-,root,root)
%_datadir/scribus/doc/fr

%files -n %name-i18n-de
%defattr(-,root,root)
%_datadir/scribus/doc/de


