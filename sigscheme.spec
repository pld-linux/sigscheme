#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	SigScheme - R5RS Scheme interpreter for embedded use
Summary(pl.UTF-8):	SigScheme - interpreter R5RS Scheme do zastosowań wbudowanych
Name:		sigscheme
Version:	0.8.6
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: https://github.com/uim/sigscheme/releases
Source0:	https://github.com/uim/sigscheme/archive/%{name}-%{version}.tar.gz
# Source0-md5:	b82819db730772abbb8824398db044bb
URL:		https://github.com/uim/sigscheme
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10
BuildRequires:	libgcroots-devel >= 0.2.3
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	libgcroots >= 0.2.3
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
Requires:	libgcroots-devel >= 0.2.3

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
%setup -q -n %{name}-%{name}-%{version}

# stub submodule
install -d libgcroots

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-maintainer-mode \
	%{!?with_static_libs:--disable-static} \
	--with-libgcroots=installed

%{__make} \
	RUBY="ruby -E utf-8"

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
%doc AUTHORS COPYING NEWS QALog README RELNOTE TODO doc/*.html
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
