# TODO
# - see if can use our js package
#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

Summary:	Check JavaScript code for common mistakes
Name:		jsl
Version:	0.3.0
Release:	1
License:	MPL v1.1
Group:		Development/Tools
URL:		http://www.javascriptlint.com/
Source0:	http://www.javascriptlint.com/download/%{name}-%{version}-src.tar.gz
# Source0-md5:	2b94ffa4fab07acabe0c5e73cd49bcdf
Patch0:		smash.patch
Patch1:		tests.patch
%{?with_tests:BuildRequires:	perl-base}
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
With JavaScript Lint, you can check all your JavaScript source code
for common mistakes without actually running the script or opening the
web page.

JavaScript Lint holds an advantage over competing lints because it is
based on the JavaScript engine for the Firefox browser. This provides
a robust framework that can not only check JavaScript syntax but also
examine the coding techniques used in the script and warn against
questionable practices.

%prep
%setup -q
find -type f | xargs %undos
%patch0 -p1
%patch1 -p1

%build
# Dependencies dealt with poorly: -j1
%{__make} -C src -f Makefile.ref -j1 \
	CC="%{__cc}" \
	XCFLAGS="%{optflags}" \
	OS_CFLAGS="-DXP_UNIX -DHAVE_VA_COPY -DVA_COPY=va_copy" \
	SHARED_LIBRARY= \
	OBJDIR=. \
	JS_EDITLINE=1 \

%if %{with tests}
cd tests
%{__perl} run_tests.pl ../src/jsl
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p src/jsl $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jsl
