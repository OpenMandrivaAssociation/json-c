%define oldmaj 0
%define major 2
%define libname %mklibname %{name} %{major}
%define libold %mklibname json %{oldmaj}
%define devname %mklibname %{name} -d
%bcond_with crosscompile

Summary:	JSON implementation in C
Name:		json-c
Version:	0.11
Release:	4
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

%package -n %{libold}
Summary:	JSON implementation in C
Group:		System/Libraries

%description -n %{libname}
This package contains the compatibility library for %{name}.

%package -n %{devname}
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Requires:	%{libold} >= %{version}-%{release}
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
%configure2_5x \
	--disable-static

make

%install
%makeinstall_std

%pre
# directory changed from file to symlink
[ $1 -gt 1 -a -d %{_includedir}/json ] && \
rm -rf %{_includedir}/json || :

%files -n %{libname}
%{_libdir}/libjson-c.so.%{major}*

%files -n %{libold}
%{_libdir}/libjson.so.%{oldmaj}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/%{name}
%{_includedir}/json
%{_libdir}/pkgconfig/*.pc
