#####################
# Hardcode PLF build
%define build_plf 0
#####################

%{?_with_plf: %{expand: %%global build_plf 1}}

%if %{build_plf}
%define distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif

Summary:	MPD, the Music Player Daemon
Name:		mpd
Version:	0.18.10
Release:	1%{?extrarelsuffix}
License:	GPLv2+
Group:		Sound
Url:		http://www.musicpd.org/
Source0:	http://www.musicpd.org/download/%{name}/%{name}-%{version}.tar.xz
Source1:	%{name}.conf
Source2:        %{name}.tmpfiles.d
Source3:	%{name}.logrotate
Source4:	README.urpmi
Source100:	%{name}.rpmlintrc
Patch0:		mpd-0.18.8-libvorbis.patch

Requires(pre,post):	rpm-helper
Requires(preun,postun): rpm-helper
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(atomic_ops)
BuildRequires:	pkgconfig(libsystemd-daemon)
BuildRequires:	pkgconfig(glib-2.0) >= 2.28
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	avahi-common-devel
BuildRequires:	pkgconfig(libcurl) >= 7.18
# sound servers
BuildRequires:	pkgconfig(alsa) >= 0.9.0
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libpulse) >= 0.9.16
BuildRequires:	pkgconfig(fluidsynth) >= 1.1
BuildRequires:	pkgconfig(libmms) >= 0.4
BuildRequires:	pkgconfig(openal)
# multimedia formats
BuildRequires:	pkgconfig(adplug)
BuildRequires:	pkgconfig(ao)
BuildRequires:	pkgconfig(audiofile) >= 0.3
BuildRequires:	pkgconfig(flac) >= 1.2
BuildRequires:	pkgconfig(flac++)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(libcdio_paranoia)
BuildRequires:	pkgconfig(libffado)
BuildRequires:	pkgconfig(libiso9660)
BuildRequires:	pkgconfig(libmodplug)
BuildRequires:	pkgconfig(libmpg123)
BuildRequires:	pkgconfig(libsidplay2)
BuildRequires:	pkgconfig(libsidutils)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(samplerate) >= 0.0.15
BuildRequires:	pkgconfig(shout)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(twolame)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(wavpack)
BuildRequires:	pkgconfig(yajl) >= 2.0
BuildRequires:	pkgconfig(zziplib) >= 0.13
BuildRequires:	ffmpeg-devel
BuildRequires:	libgme-devel
BuildRequires:	libmikmod-devel
BuildRequires:	libmpcdec-devel
BuildRequires:	wildmidi-devel

%if %{build_plf}
BuildRequires:	libfaad2-devel
BuildRequires:	lame-devel
%endif

%description
Music Player Daemon (MPD) allows remote access for playing music (MP3, Ogg
Vorbis, FLAC, Mod, and wave files) and managing play-lists. MPD is designed
for integrating a computer into a stereo system that provides control for music
playback over a local network. It is also makes a great desktop music player,
especially if you are a console junkie, like front-end options, or restart X
often.
%if %{build_plf}
This package is in restricted repository because it is built with AAC support
of libfaad2, which is patent-protected.
%endif


%prep
%setup -q
%patch0 -b .vorbis
autoreconf -vfi


%build
# Mad and sidplay option make the build to fail
%configure2_5x \
	--with-systemdsystemunitdir=%{_unitdir} \
	--with-zeroconf=auto \
	--enable-alsa \
	--enable-ao \
	--enable-audiofile \
	--enable-cdio-paranoia \
	--enable-curl \
	--enable-flac \
	--enable-ffmpeg \
	--enable-fluidsynth \
	--enable-gme \
	--enable-id3 \
	--enable-iso9660 \
	--enable-jack \
	--enable-soundcloud \
	--enable-lsr \
	--disable-mad \
	--enable-mikmod \
	--enable-mms \
	--enable-modplug \
	--enable-mpg123 \
	--enable-openal \
	--enable-opus \
	--enable-pulse \
	--enable-recorder-output \
	--disable-roar \
	--enable-shout \
	--disable-sidplay \
	--enable-sndfile \
	--enable-twolame-encoder \
	--enable-vorbis \
	--enable-vorbis-encoder \
	--enable-wave-encoder \
	--enable-wavpack \
	--enable-wildmidi \
	--enable-zzip \
%if !%{build_plf}
	--disable-aac \
	--disable-lame-encoder \
%endif
	--enable-sqlite
%make


%install
%makeinstall_std

mkdir -p %{buildroot}/var/lib/mpd
touch %{buildroot}/%{_localstatedir}/lib/mpd/mpd.db
touch %{buildroot}/%{_localstatedir}/lib/mpd/mpdstate
mkdir -p %{buildroot}/var/log/mpd
touch %{buildroot}/var/log/mpd/mpd.log
touch %{buildroot}/var/log/mpd/mpd.error
mkdir -p %{buildroot}/var/run/mpd
mkdir -p %{buildroot}/%{_localstatedir}/lib/mpd/playlists
mkdir -p %{buildroot}/%{_localstatedir}/lib/mpd/music
mkdir -p %{buildroot}/lib/systemd/system

install -D -m 644 %{SOURCE1} %{buildroot}/etc/mpd.conf
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m 644 %{SOURCE4} doc/README.urpmi
rm -rf %{buildroot}/%{_docdir}/mpd

install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_tmpfilesdir}/mpd.conf

%pre
%_pre_useradd %{name} %{_localstatedir}/lib/%{name} /bin/false
usermod -g audio %{name}


%post
if [ $1 -eq 1 ]
then
%create_ghostfile %{_localstatedir}/lib/mpd/mpd.db mpd audio 644
%create_ghostfile %{_localstatedir}/lib/mpd/mpdstate mpd audio 644
%create_ghostfile /var/log/mpd/mpd.log mpd audio 644
%create_ghostfile /var/log/mpd/mpd.error mpd audio 644
fi
%_post_service %{name}


%preun
%_preun_service %{name}


%postun
%_postun_userdel %{name}


%files
%doc README UPGRADING AUTHORS NEWS doc/mpdconf.example doc/*.urpmi
%{_bindir}/%{name}
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_tmpfilesdir}*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,mpd,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%defattr(644,mpd,audio)
%attr(755,mpd,audio) %dir %{_localstatedir}/lib/mpd
%attr(755,mpd,audio) %dir %{_localstatedir}/lib/mpd/music
%attr(755,mpd,audio) %dir %{_localstatedir}/lib/mpd/playlists
%ghost %{_localstatedir}/lib/mpd/mpd.db
%ghost %{_localstatedir}/lib/mpd/mpdstate
%attr(755,mpd,audio) %dir /var/log/mpd
%attr(755,mpd,audio) %dir /var/run/mpd
%ghost /var/log/mpd/mpd.log
%ghost /var/log/mpd/mpd.error
%attr(644,root,root) /lib/systemd/system/%{name}.service

%changelog
* Fri Mar 28 2014 Giovanni Mariani <mc2374@mclink.it> 0.18.9-2
- Fixed typo in configure making the package wrongly depend upon lame
  library (in Restricted)

* Sat Mar 22 2014 Giovanni Mariani <mc2374@mclink.it> 0.18.9-1
- New release 0.18.9
- Updated Source0 and URL tags
- Taken P0 from Mageia
- Updated BReqs list to enable more format support (from Mageia)
  and enabled them in the configure options
- Added S100 to silence many (useless or wrong) rpmlint warnings