%define name    scribus
%define version 1.3.3.9
%define rel     5
%define release %mkrel %{rel}

%define	major	0
%define	libname	%mklibname %name %major
%define develname %{name}-devel

Summary: 	Scribus - Open Source Page Layout
Name: 		%name
Version: 	%version
Release:	%release
Source0:	http://downloads.sourceforge.net/scribus/scribus-%{version}.tar.bz2
URL: 		http://www.scribus.net/
License:	GPL
Group:  	Office
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	autoconf
BuildRequires:	cups-devel
BuildRequires:	lcms-devel
BuildRequires:	libart_lgpl-devel
BuildRequires:	libcairo-devel
BuildRequires:	qt3-devel
BuildRequires:	tiff-devel
BuildRequires:	python-devel
BuildRequires:	libtiff-devel
BuildRequires:	cmake

Requires:	tkinter
Requires:	ghostscript-common

Obsoletes:	kde3-scribus 
Provides:	kde3-scribus

Obsoletes:    scribus-i18en
Obsoletes:    scribus-i18de
Obsoletes:    scribus-i18fr
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

%post
%update_menus
%update_mime_database

%postun
%clean_menus
%clean_mime_database

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*
#%{_datadir}/pixmaps/*
%{_libdir}/scribus
%{_datadir}/mime/packages/*.xml
%{_datadir}/scribus

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

%build
%cmake

%make -j1

%install
rm -rf $RPM_BUILD_ROOT

# Laurent don't use %%makeinstall it doesn't work
# lib and pugins in not install in good directory.
cd build
%makeinstall_std
cd -

install -d %buildroot%{_datadir}/applications
install scribus.desktop %buildroot%{_datadir}/applications/

# fwang: cp include files now
# or, not needed??
install -d %buildrot%{_includedir}/%{name}
install %{name}/*.h %buildrot%{_includedir}/%{name}/

%clean
rm -rf $RPM_BUILD_ROOT
