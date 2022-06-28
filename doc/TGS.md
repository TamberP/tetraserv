# TGS Notes

Look, I'm legit reverse-engineering this because I feel hilariously
awkward just asking for some documentation on it. Anyway!

With the v5 API:
- TGS pokes at the DM world via Topic() and gets very basic responses back via topic-response.
- DM world does most of its communication with TGS via Bridge requests

## Bridge

The Bridge is a localhost http-only server. Communication is initiated
by making a world.Export() call to the bridge, passing data in
urlencoded JSON in the request query string. Bridge then responds with
more JSON.

a *lot* of the TGS commands *will not work at all* unless the initial
communication with the bridge, during world initialisation, succeeds
and the runtime information is decoded.

The bridge port & `tgs_key` is passed in *on the DreamMaker
command-line*, via the `-param` argument string, when TGS starts
DreamMaker.

e.g. `DreamDaemon <DMB> 42069 -invisible -trusted -params "server_service_version=5.2.4&tgs_port=42070&tgs_key='boop'"`

Fun side note: The `tgs_key`, in standard tgstation-server, is a
random string generated at DM server startup time; rather than loaded from a config.

### Bridge commands

(Get the request, urlparse the request, parse the query arguments.)

the `data` arg contains the TGS data. Within that:
- `accessIdentifier` - This should match `tgs_key`.
- `commandType`
    + Type 0: Port update request.
    + Type 1: World requests runtime information.
    + Type 2: World initialisation complete ("Primed")
    + Type 3: Reboot request
    + Type 4: Shutdown request
    + Type 5: WorldChat send

### Runtime Information

Contains information such as the API version of the Bridge server, the
security level the DM World is running under (0: trusted), the name of
the world ("Scrunge Laboratories XIII"), revision information, a list
of test-merge revision info, and a list of channels.

### WorldChat

`tgs_data["chatMessage"]` contains json with:
+ `text`: The message
+ `channelIds`: A list of IDs of which channels the message is to be
sent to. The id matches with one of the channels specified in the
runtime info.
