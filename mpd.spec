#####################
# Hardcode PLF build
%define build_plf 1
#####################
%{?_with_plf: %{expand: %%global build_plf 1}}

%if %{build_plf}
%define distsuffix plf
# Make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif

%define majorver %(echo %{version} | cut -d. -f 1-2)

Summary:		The Music Player Daemon
Name:		mpd
Version:		0.24.14
Release:		101
License:		GPLv2+
Group:		Sound
Url:		https://www.musicpd.org/
Source0:	https://www.musicpd.org/download/mpd/%{majorver}/%{name}-%{version}.tar.xz
Source1:	%{name}.conf
Source2:	%{name}.tmpfiles.d
Source3:	%{name}.sysusers.d
Source4:	%{name}.logrotate
Source100:	%{name}.rpmlintrc
Patch0:		mpd-0.24.4-fix-mpcdec-header-path.patch
BuildRequires:		meson
BuildRequires:		ninja
BuildRequires:		python-sphinx
BuildRequires:		systemd
BuildRequires:		avahi-common-devel
BuildRequires:		boost-devel
BuildRequires:		boost-core-devel
BuildRequires:		pkgconfig(atomic_ops)
BuildRequires:		pkgconfig(avahi-client)
BuildRequires:		pkgconfig(avahi-glib)
BuildRequires:		pkgconfig(bzip2)
BuildRequires:		pkgconfig(dbus-1)
BuildRequires:		pkgconfig(expat)
BuildRequires:		pkgconfig(glib-2.0) >= 2.28
BuildRequires:		pkgconfig(gthread-2.0)
BuildRequires:		pkgconfig(icu-i18n)
BuildRequires:		pkgconfig(libchromaprint)
BuildRequires:		pkgconfig(libcurl) >= 7.18
BuildRequires:		pkgconfig(libffado)
BuildRequires:		pkgconfig(libgcrypt)
BuildRequires:		pkgconfig(libmpdclient)
BuildRequires:		pkgconfig(libpcre2-8)
BuildRequires:		pkgconfig(liburing)
BuildRequires:		pkgconfig(udisks2)
BuildRequires:		pkgconfig(libupnp)
BuildRequires:		pkgconfig(nlohmann_json)
%ifnarch %{ix86} %{arm}
BuildRequires:		pkgconfig(smbclient)
%endif
BuildRequires:		pkgconfig(sqlite3)
BuildRequires:		pkgconfig(systemd)
BuildRequires:		pkgconfig(udisks2)
BuildRequires:		python3dist(sphinx)
# Sound servers
# This is in Extra ATM
BuildRequires:		pkgconfig(adplug)
BuildRequires:		pkgconfig(alsa) >= 0.9.0
BuildRequires:		pkgconfig(fluidsynth) >= 1.1
BuildRequires:		pkgconfig(fmt)
BuildRequires:		pkgconfig(jack)
BuildRequires:		pkgconfig(libmms) >= 0.4
BuildRequires:		pkgconfig(libpipewire-0.3)
BuildRequires:		pkgconfig(libpulse) >= 0.9.16
BuildRequires:		pkgconfig(openal)
# Multimedia formats
BuildRequires:		pkgconfig(lame)
BuildRequires:		pkgconfig(libavformat)
BuildRequires:		pkgconfig(libavcodec)
BuildRequires:		pkgconfig(libavfilter)
BuildRequires:		pkgconfig(libavutil)
BuildRequires:		libmp4v2-devel
# Version in cooker is too old
#BuildRequires:		libmpcdec-devel
BuildRequires:		wrap-devel
BuildRequires:		pkgconfig(ao)
BuildRequires:		pkgconfig(audiofile) >= 0.3
BuildRequires:		pkgconfig(flac) >= 1.2
BuildRequires:		pkgconfig(flac++)
BuildRequires:		pkgconfig(id3tag)
BuildRequires:		pkgconfig(libcdio_paranoia)
BuildRequires:		pkgconfig(libgme)
BuildRequires:		pkgconfig(libiso9660)
BuildRequires:		pkgconfig(libmikmod)
BuildRequires:		pkgconfig(libmodplug)
BuildRequires:		pkgconfig(libmpg123)
BuildRequires:		pkgconfig(libnfs)
# This is in Extra ATM
%if %{build_plf}
BuildRequires:		pkgconfig(faad2)
%endif
BuildRequires:		pkgconfig(libopenmpt)
BuildRequires:		pkgconfig(libsidplayfp)
BuildRequires:		pkgconfig(libsoup-3.0)
BuildRequires:		pkgconfig(libupnp)
BuildRequires:		pkgconfig(mad)
BuildRequires:		pkgconfig(ogg)
BuildRequires:		pkgconfig(opus)
BuildRequires:		pkgconfig(samplerate) >= 0.0.15
BuildRequires:		pkgconfig(shout)
BuildRequires:		pkgconfig(sndfile)
BuildRequires:		pkgconfig(sndio)
BuildRequires:		pkgconfig(soxr)
BuildRequires:		pkgconfig(twolame)
BuildRequires:		pkgconfig(vorbis)
BuildRequires:		pkgconfig(vorbisenc)
BuildRequires:		pkgconfig(vorbisfile)
BuildRequires:		pkgconfig(wavpack)
BuildRequires:		pkgconfig(wildmidi)
BuildRequires:		pkgconfig(yajl) >= 2.0
BuildRequires:		pkgconfig(zlib)
BuildRequires:		pkgconfig(zziplib) >= 0.13
Requires(pre,preun):		systemd
Requires(pre,post):	rpm-helper
Requires(preun,postun):	rpm-helper
Requires:	logrotate

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

%files
%doc README.md AUTHORS NEWS doc/mpdconf.example
 %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,mpd,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_mandir}/man5/%{name}.conf.5*
%{_tmpfilesdir}/%{name}.conf
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%defattr(644,mpd,audio)
%attr(755,mpd,audio) %dir %{_localstatedir}/lib/%{name}
%attr(755,mpd,audio) %dir %{_localstatedir}/lib/%{name}/music
%attr(755,mpd,audio) %dir %{_localstatedir}/lib/%{name}/playlists
%ghost %{_localstatedir}/lib/%{name}/%{name}.db
%ghost %{_localstatedir}/lib/%{name}/mpdstate
%attr(755,mpd,audio) %dir /var/log/%{name}
#attr(755,mpd,audio) %%dir /var/run/%%{name}
%ghost /var/log/mpd/%{name}.log
%ghost /var/log/mpd/%{name}.error
%ghost /run/mpd
%{_presetdir}/86-%{name}.preset
%attr(644,root,root) %{_unitdir}/%{name}.service
%attr(644,root,root) %{_unitdir}/%{name}.socket
%attr(644,root,root) %{_userunitdir}/%{name}.service
%attr(644,root,root) %{_sysusersdir}/%{name}.conf
%attr(644,root,root) %{_prefix}/lib/systemd/user/%{name}.socket

%pre
%sysusers_create_package %{name} %{SOURCE3}

%post
# This is a workaround for the mpd user being created
# with the wrong home directory in earlier versions of the package.
# Fixed after 5.0 -- the workaround should be removed
# when we stop supporting updating from <= 5.0
groupdel mpd &>/dev/null || :
userdel mpd &>/dev/null || :
systemd-sysusers %{_sysusersdir}/%{name}.conf
if [ $1 -eq 1 ]
then
%create_ghostfile %{_localstatedir}/lib/%{name}/%{name}.db mpd audio 644
%create_ghostfile %{_localstatedir}/lib/%{name}/mpdstate mpd audio 644
%create_ghostfile %{_localstatedir}/log/%{name}/%{name}.log mpd audio 644
%create_ghostfile %{_localstatedir}/log/%{name}/%{name}.error mpd audio 644
fi
%tmpfiles_create %{_tmpfilesdir}/%{name}.conf
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

#-----------------------------------------------------------------------------

%prep
%autosetup -p1


%build
# Adplug and libopenmpt are in Extra
# Our libmpcdec lacks mpc_demux_init: it's too old
%meson \
			-Dadplug=enabled \
			-Dalsa=enabled \
			-Dao=enabled \
			-Daudiofile=enabled \
			-Dbzip2=enabled \
			-Dcdio_paranoia=enabled \
			-Dchromaprint=enabled \
			-Dcue=true \
			-Dcurl=enabled \
			-Ddaemon=true \
			-Ddatabase=true \
			-Ddsd=true \
		%if !%{build_plf}
			-Dfaad=disabled \
		%endif
			-Dflac=enabled \
			-Dffmpeg=enabled \
			-Dfluidsynth=enabled \
			-Dgme=enabled \
			-Did3tag=enabled \
			-Dinotify=true \
			-Dio_uring=enabled \
			-Diso9660=enabled \
			-Djack=enabled \
			-Dlame=enabled \
			-Dlibmpdclient=enabled \
			-Dmad=enabled \
			-Dmikmod=enabled \
			-Dmms=enabled \
			-Dmodplug=enabled \
			-Dmpcdec=disabled \
			-Dmpg123=enabled \
			-Dneighbor=true \
			-Dopenal=enabled \
			-Dopenmpt=enabled \
			-Dopus=enabled \
			-Dpulse=enabled \
			-Drecorder=true \
			-Dshine=disabled \
			-Dshout=enabled \
			-Dsidplay=enabled \
		%ifarch %{ix86} %{arm}
			-Dsmbclient=disabled \
		%endif
			-Dsndfile=enabled \
			-Dsndio=enabled \
			-Dsolaris_output=disabled \
			-Dsqlite=enabled \
			-Dtremor=disabled \
			-Dtwolame=enabled \
			-Dudisks=enabled \
			-Dupnp=auto \
			-Dvorbis=enabled \
			-Dvorbisenc=enabled \
			-Dwave_encoder=true \
			-Dwavpack=enabled \
			-Dwildmidi=enabled \
			-Dzeroconf=auto \
			-Dzzip=enabled \
			-Dsystemd_system_unit_dir=%{_unitdir} \
			-Dsystemd_user_unit_dir=%{_userunitdir}

%meson_build


%install
%meson_install

# Create various needed dirs
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}%{_localstatedir}/run/%{name}
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/playlists
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/music
mkdir -p %{buildroot}/lib/systemd/system
mkdir -p %{buildroot}%{_sysusersdir}/
mkdir -p %{buildroot}%{_presetdir}

# Create ghost files
touch %{buildroot}%{_localstatedir}/lib/%{name}/%{name}.db
touch %{buildroot}%{_localstatedir}/lib/%{name}/mpdstate
touch %{buildroot}%{_localstatedir}/log/%{name}/%{name}.log
touch %{buildroot}%{_localstatedir}/log/%{name}/%{name}.error

# Install our config stuff
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.conf
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.conf
install -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Create a preset
cat > %{buildroot}%{_presetdir}/86-mpd.preset << EOF
enable mpd.socket
EOF

# We pick the docs with our macro
rm -rf %{buildroot}/%{_docdir}/%{name}
