%define name    scribus
%define version 1.3.3.9
%define rel     1
%define release %mkrel %{rel}

%define	major	0
%define	libname	%mklibname %name %major

Summary: 	Scribus - Open Source Page Layout
Name: 		%name
Version: 	%version
Release:	%release
Source0:	http://downloads.sourceforge.net/scribus/scribus-%{version}.tar.bz2
URL: 		http://www.scribus.net/
License:	GPL
Group:  	Office
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	autoconf2.5
BuildRequires:	cups-devel
BuildRequires:	lcms-devel
BuildRequires:	libart_lgpl-devel
BuildRequires:	libcairo-devel
BuildRequires:	qt3-devel
BuildRequires:	tiff-devel

Requires:	%libname = %version
Obsoletes:	kde3-scribus 
Provides:	kde3-scribus

Obsoletes:    scribus-i18en
Obsoletes:    scribus-i18de
Obsoletes:    scribus-i18fr

%description
Scribus is a desktop open source page layout program with the aim of
producing commerical grade output in PDF and Postscript, primarily,
though not exclusively, for Linux.

While the goals of the program are ease of use and simple
easy-to-understand tools, Scribus offers support for professional
publishing features, such as CMYK colors, easy PDF creation,
Encapsulated Postscript import and export, and creation of color
separations.

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

%prep
%setup -q

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

%make

%install
rm -rf $RPM_BUILD_ROOT

# Laurent don't use %%makeinstall it doesn't work
# lib and pugins in not install in good directory.
%makeinstall

install -d %buildroot{_datadir}/applications
install scribus.desktop %buildroot{_datadir}/applications/
install -d %buildroot{_datadir}/mime/packages
install scribus.xml %buildroot {_datadir}/mime/packages/scribus.xml

%post
%update_menus
%update_mime_database

%postun
%clean_menus
%update_mime_database

%post -n %{libname} -p /sbin/ldconfig                                                                                                        
%postun -n %{libname} -p /sbin/ldconfig                                                                                                      

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README TODO BUILDING ChangeLogCVS INSTALL NEWS PACKAGING README.MacOSX
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_mandir}/*/*
%{_datadir}/pixmaps/*
%{_libdir}/scribus
%{_datadir}/mime/packages/*.xml
%{_datadir}/share/scribus
%{_docdir}/scribus
%lang(pl) %dir %{_mandir}/pl
%lang(pl) %dir %{_mandir}/pl/man1

%files -n %{libname}-devel
%defattr(-,root,root)
%doc AUTHORS COPYING
%_includedir/%name/*
