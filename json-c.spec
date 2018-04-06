%define oldmaj 0
%define major 3
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%bcond_with crosscompile

Summary:	JSON implementation in C
Name:		json-c
Version:	0.13.1
Release:	1
Group:		System/Libraries
License:	MIT
Url:		https://github.com/json-c/json-c/wiki
Source0:	https://s3.amazonaws.com/json-c_releases/releases/%{name}-%{version}.tar.gz
BuildRequires:	libtool

%description
JSON-C implements a reference counting object model that allows you to
easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C
representation of JSON objects.

%package -n %{libname}
Summary:	JSON implementation in C
Group:		System/Libraries

%description -n %{libname}
JSON-C implements a reference counting object model that allows you to
easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C
representation of JSON objects.

%package -n %{devname}
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}json-devel < 0.11-2

%description -n %{devname}
JSON-C implements a reference counting object model that allows you to
easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C
representation of JSON objects.

%prep
%setup -q

%if %{with crosscompile}
export ac_cv_func_malloc_0_nonnull=yes
%endif

%build
sed -i -e "s:-Werror::" configure.ac
autoreconf -fiv
%configure \
	--disable-static

%make

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/libjson-c.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/%{name}
%{_libdir}/pkgconfig/*.pc
