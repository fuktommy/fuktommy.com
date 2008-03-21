function FindProxyForURL(url, host) {
    if (dnsDomainIs(host, "2ch.net") ||
        dnsDomainIs(host, "bbspink.com") ||
        dnsDomainIs(host, "local.tubo.img")) {
        return "PROXY localhost:8095";
    } else {
        return "DIRECT";
    }
}
