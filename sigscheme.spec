#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	SigScheme - R5RS Scheme interpreter for embedded use
Summary(pl.UTF-8):	SigScheme - interpreter R5RS Scheme do zastosowań wbudowanych
Name:		sigscheme
Version:	0.8.5
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://code.google.com/p/sigscheme/downloads/list
Source0:	http://sigscheme.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	396f12ee8d4102a59723c845a110b07d
URL:		http://code.google.com/p/sigscheme/wiki/libgcroots
BuildRequires:	libgcroots-devel >= 0.1.4
BuildRequires:	pkgconfig
Requires:	libgcroots >= 0.1.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SigScheme is a R5RS Scheme interpreter for embedded use.

%description -l pl.UTF-8
SigScheme to interpreter R5RS Scheme do zastosowań wbudowanych.

%package devel
Summary:	Header files for SigScheme library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SigScheme
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libgcroots-devel >= 0.1.4

%description devel
Header files for SigScheme library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SigScheme.

%package static
Summary:	Static SigScheme library
Summary(pl.UTF-8):	Statyczna biblioteka SigScheme
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SigScheme library.

%description static -l pl.UTF-8
Statyczna biblioteka SigScheme.

%prep
%setup -q

%build
%configure \
	%{!?with_static_libs:--disable-static} \
	--with-libgcroots=installed
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/sigscheme

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS QALog README doc/*.html
%attr(755,root,root) %{_bindir}/sscm
%attr(755,root,root) %{_libdir}/libsscm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsscm.so.3
%{_datadir}/sigscheme

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsscm.so
%{_includedir}/sigscheme
%{_pkgconfigdir}/sigscheme.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsscm.a
%endif
