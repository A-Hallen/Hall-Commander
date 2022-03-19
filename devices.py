import pyudev


class Devices:
    def __init__(self):
        self.lista2 = {}
        self.lista = {}
        self.index = 0

    def return_dict(self):
        self.list_volumes()
        return self.lista

    def list_volumes(self):
        from gi.repository import Gio
        volumen_monitor = Gio.VolumeMonitor.get()
        for volume in volumen_monitor.get_volumes():
            name = volume.get_name()
            drive = volume.get_drive()
            mount = volume.get_mount()
            uuid = volume.get_identifier(Gio.VOLUME_IDENTIFIER_KIND_LABEL)
            if uuid is None:
                uuid = volume.get_identifier(Gio.VOLUME_IDENTIFIER_KIND_UUID)
            uuid = str(uuid)

            if mount is None:
                mount_point = ""
            else:
                mount_point = mount.get_default_location().get_parse_name()
            if drive is None:
                removable = True
            else:
                removable = drive.can_eject()

            tipo = ""
            uri = ""
            activation_root = volume.get_activation_root()
            if activation_root:
                uri = activation_root.get_uri()
                tipo = activation_root.get_uri_scheme()
                mount_point = self.check_mtp_montpoint(uri)

            fullname = volume.get_identifier(Gio.VOLUME_IDENTIFIER_KIND_UNIX_DEVICE)
            if tipo == "":
                context = pyudev.Context()
                for device in context.list_devices():
                    if device.get('DEVNAME', "Unknown") == fullname:
                        if 'ID_BUS' in device.keys():
                            tipo = device['ID_BUS']
            # '372 GB Volume': ['7AB20E9EB20E5F4F', 'ata', '/media/hallen/sda3', '/dev/sda3', False]
            self.lista[name] = [uuid, tipo, mount_point, fullname, removable, uri]

    @staticmethod
    def check_mtp_montpoint(uri):
        import os
        retorno = ""
        mount_path = os.path.join(os.path.join('/run/user/', str(os.getuid())), 'gvfs/')
        if os.path.exists(mount_path) and os.path.isdir(mount_path):
            lista = os.listdir(mount_path)
            for file in lista:
                new = file.replace("mtp:host=", "")
                if new in uri:
                    return mount_path + file

        return retorno

    @staticmethod
    def monitoring():
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by('block')
        for device in iter(monitor.poll, None):
            if device.action == 'add':
                print("connected")
            else:
                print('{0.action} on {0.device_path}'.format(device))
