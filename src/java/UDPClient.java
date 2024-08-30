// package your.package.name;
import android.graphics.Bitmap;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;

public class UDPClient implements Runnable {
    DatagramSocket socket;
    String S_IP;
    final int S_PORT;
    final int chunkSize;
    byte[] data;
    int nextPacketIndex;
    boolean free;

    public UDPClient(int c_port, int s_port) {
        try {
            socket = new DatagramSocket(c_port);
        } catch (SocketException e) {
            e.printStackTrace();
        }
        S_PORT = s_port;
        chunkSize = 1018;
        nextPacketIndex = 255;
        free = true;
    }

    @Override
    public void run() {
        try {
            // Send image data in chunks of 1024 bytes
            for (int i = 0, j = 0; i < data.length; i += chunkSize, j++) {
                byte[] chunk = new byte[6 + Math.min(chunkSize, data.length - i)];
                System.arraycopy(packetHeader(nextPacketIndex, j, data.length), 0, chunk, 0, 6);
                System.arraycopy(data, i, chunk, 6, chunk.length - 6);
                DatagramPacket packet = new DatagramPacket(chunk, chunk.length, InetAddress.getByName(S_IP), S_PORT);
                socket.send(packet);
            }
        }
        catch (IOException e) {
            e.printStackTrace();
        }
        free = true;
    }

    public void Send(Bitmap bitmap, String ip, int cameraFacing) {
        if (!free)
            return;
        free = false;
        S_IP = ip;
        nextPacketIndex = (nextPacketIndex + 1) % 256;
        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 50, stream);
        byte[] img = stream.toByteArray();
        byte[] cameraByte = new byte[]{(byte) cameraFacing};
        data = new byte[1 + img.length];
        System.arraycopy(cameraByte, 0, data, 0, 1);
        System.arraycopy(img, 0, data, 1, img.length);
        new Thread(this).start();
    }

    byte[] packetHeader(int globalIndex, int localIndex, int len) {
        return new byte[] {
                (byte)globalIndex,
                (byte)(localIndex >>> 8),
                (byte)localIndex,
                (byte)(len >>> 16),
                (byte)(len >>> 8),
                (byte)len};
    }
}