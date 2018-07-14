## 4 thành phần của Embedded Linux

Ta biết rằng Linux chạy ở khắp nơi từ siêu máy tính, máy chủ, máy để bàn (máy xách tay), điện thoại (android)...cho đến các thiết bị gia dụng.

Khi sử dụng máy tính cá nhân, server ta dễ dàng "sờ" thấy được các thành phần của Linux như các tiến trình, shell..etc.  
Hầu hết các bản phân phối phổ biến làm hết những thứ liên quan đến phần cứng, nhân hệ điều hành, driver cho ta rồi. Ta thường chỉ quan tâm đến ứng dụng chạy trên đó thôi.

Nhưng ở một mảng ứng dụng khác của Linux, nơi mà trên đó ta thường chỉ chạy 1 ứng dụng, rất khó thấy các thành phần bên trong, hầu như không thay đổi được...thì Linux như thế nào, nó giống với các bản phân phối ta vẫn gặp không.

Rồi thêm nữa, trên quan điểm của một "coder", thì người ta phát triển thiết bị chạy Linux kiểu đó như thế nào.

Bài  **cưỡi ngựa xem hoa**  này chỉ nói về các thành phần mà người ta phải nghĩ đến khi phát triển một ứng dụng trên một phần cứng mới. Tất nhiên, hầu hết chúng ta sẽ phát triển ứng dụng, ít động đến những phần đó. Nhưng có một hiểu biết tổng quan sẽ khá thú vị.

## 1\. Toolchain - compiler, linker, sysroot...

**Tại sao lại phải quan tâm đến toolchain ngay từ đầu, và toolchain là cái gì?**

Trước khi nói về Toolchain, ta hãy nói chút về những thành phần cơ bản để tạo ra một ứng dụng trên Linux.

Như chúng ta đã biết, để chạy một đoạn code C (ngôn ngữ nào khác) bất kì, dù đơn giản đến đâu đi nữa, thì ta phải biên dịch nó ra mã nhị phân mà máy tính hiểu được. Việc biên dịch đó cần một phần mềm gọi là  `Compiler`.

Một thành phần nữa gần như tối thiểu là  `C library`  hay gọi là thư viện chuẩn của C ấy. Lý do gọi là gọi là chuẩn là bởi vì tuân theo một chuẩn giao diện nhất định ví dụ POSIX chẳng hạn. Người ta chỉ implment các giao diện đó theo cách hoạt hoạt động của Linux mà thôi.  
Trên Linux, các hàm thư viện C thực chất là  `wrapper đến system call`  (tạm dịch là lời gọi hệ thống). Do các system call quá khó để sử dụng và không portabilily (tức là mỗi CPU có lại có một cách gọi system call khác nhau).  
Hầu hết các ứng dụng từ I/O, Network đều sử dụng thư viện chuẩn C này nên nó gần như là tối thiểu. Thư viện này cũng thường được xây dựng kèm theo  `Compiler`  luôn.

Để liên kết những thứ đó lại rồi tạo ra 1 file nhị phân có thể chạy được thì cần đến một  `Linker`  hoặc  `Dynamic loader-linker`.

Rồi từ code C không chỉ 1 bước là biến thành mã máy, nó phải chuyển sang mã Assembly rồi dùng chuyển từ mã Assembly đó ra mã máy. Việc đó ít nhất còn cần 1 thêm 1  `Compiler`  cho Assembly nữa.

Vì con người đã không còn viết trực tiếp mã nhị phân cho máy tính nữa nên bất cứ phần mềm nào từ bootloader, kernel, rồi lệnh ls, lệnh copy...etc đều phải được biên dịch ra mã nhị phân mới nhét vào máy tính chạy được.

Xin trích từ slide tham khảo bên dưới:  
`Nếu không thể tạo ra mã nhị phân cho nền tảng tính toán (platform) thì ta vẫn chỉ có 1 "phần cứng" với đúng nghĩa đen của nó mà thôi`.

**Vậy Toolchain cho Linux chung là gì?**

Nó ít nhất bao gồm những thành phần sau:

-   binutils (công cụ xử lý liên quan đến mã nhị phân): GNU Assembler, Linker, etc.
-   gcc: GNU C Compiler
-   C library (libc): gồm các file header lẫn các file binary cho phép ứng dụng giao tiếp với hệ điều hành.
-   gdb: Debugger

Nói chung, có 2 loại Toolchain là  `Native`  và  `Cross`  chia theo mối quan hệ giữa môi trường nó chạy và môi trường nó sinh mã nhị phân cho:

-   `Native`  : tức là chạy trên máy nào, sinh mã nhị phân chạy cho máy ấy luôn  
    Ví dụ các bản phân phối ta vẫn dùng có thể coi như sử dụng  _Native Toolchain_
    
-   `Cross`: tức là chạy trên một máy, nhưng sinh mã nhị phân cho máy khác.
    

Khi phát triển Embedded Linux, hầu hết chúng ta sẽ sử dụng  `Cross Toolchain`.  
Vì các thiết bị chạy thường tốc độ thấp, bộ nhớ ít nên không thích hợp để build source trên đó hay chạy  `Native Tool`  trên đó.

**C Library**

Hay chính  `glibc`  ta vẫn thấy trên các distro, thường được kèm theo GCC cho Platform tương ứng luôn.

Có 3 lựa chọn của thư viện này:

-   **GNU glibc**: đầy đủ chức năng của glibc, nhưng kích thước lớn và chạy cũng tốn
-	**GNU eglib**: vẫn là glibc, nhưng dễ configure hơn, dễ sử dụng ở hệ thống Embedded
-   **uClibc:**  nhỏ, không được update thư viện liên quan đến thread và các hàm POSIX khác

**Các tiêu chí để chọn một Toolchain**

-   Có hỗ trợ tốt platform của bạn không: ví dụ hỗ trợ kiến trúc ARM nào, ...có là soft-float hay hardfloat.
-   Có thư viện C phù hợp với yêu cầu dự án không.
-   Có được cập nhật không
-   Có được hỗ trợ tốt (từ cộng đồng hoặc thương mại) không
-   Các công cụ kèm theo có  **ngon**  không

**Vấn đề khi sử dụng thư viện**

Có nhiều Toolchain chỉ cung cấp đúng cái thư viện chuẩn C thôi.

**Nếu muốn sử dụng một thư viện nào khác thì sao?**  
Bạn có thể may mắn nếu tìm được bản build của thư viện đó cho platform của bạn đã được tác giả hoặc người khác cung cấp rồi.

Trường hợp xấu nhất, phải lấy source về tự build. Nếu thư viện được viết tốt thì không vấn đề gì, nhưng trường hợp xấu nhất là không build được. =)).

Vì thế, sẽ tốt hơn nếu chọn Toolchain mà hỗ trợ nhiều thư viện.

**Vấn đề với debug**

Đã phát triển phần mềm thì việc có bug và phải fix nó là chuyện đương nhiên.

Debug luôn là một phần trong phát triển, thậm chí có ý nghĩa rất quan trọng tới việc một dự án có kịp hay không. Vì một lỗi không thể fix có thể kéo theo một loạt hệ quả khác.  
Kiểu như chức năng A chưa fixed được các chức năng B, C, D chưa thể test hoặc có test nhưng độ tin tưởng sẽ thấp chẳng hạn. Dễ bị móm lắm.

Khi làm việc với Embedded Linux, ta nên xem xét xem toolchain có một  _gdb_  (`gdb client`) chạy ở một máy (khác với phần cứng thật) và một  `gdb server`  (chạy trên thiết bị thật) hay không để biết được có thể debug từ xa cho thiết bị hay không. Bí lắm có khi phải debug ứng dụng trên một nền tảng khác trước khi thực sự chạy trên thiết bị.

**Một vài công cụ trợ giúp khác**

Một số công cụ dưới đây nếu có sẽ làm quá trình phát triển thuận lợi hơn rất nhiều.

-   Một vài công cụ khác như Profiler - Công cụ đánh giá hiệu năng ứng dụng dựa trên  `perf`
-   Tracer thường dựa trên  `strace`
-   Plugin cho Eclipse...

## 2\. Bootloader - Nhiệm vụ duy nhất là load kernel vào RAM

**Tại sao lại cần bootloader, và bootloader là cái gì**

Trước hết nó cũng là phần mềm giống hệ điều hành, hay các ứng dụng ta vẫn đang chạy hàng ngày thôi.

Ta đã biết rằng ứng dụng của ta chạy trên hệ điều hành chứ có chạy trên bootloader đâu.  
**Vậy bootloader là cái gì??? Có nhất thiết phải cần nó???**

Nếu nói hệ điều hành chung, ngoài Linux, bao gồm các hệ điều hành cực nhỏ, giống như mấy RTOS chẳng hạn, thì có thể không cần cái bootloader ta đang nói ở đây.  
Vì thường CPU có khả năng load một đoạn code nhất định, nếu hệ điều hành đủ nhỏ để CPU load được nó lên bộ nhớ thì không cần bootloader nữa.

**Vậy kết cục, bootloader làm gì???**  
Nguyên nhân chính là từ nguyên lý cơ bản về máy tính (không nhớ rõ tên lắm).  
Đại ý là:  **chương trình phải được load lên bộ nhớ rồi mới chạy được**.

CPU thường cũng có sẵn một đoạn code nhỏ được chạy sau khi được cắm điện.  
Đoạn code này thường một đoạn cố định ở đâu đó (thường là boot sector trên main storage) vào bộ nhớ để chạy.  
*Ta nên phân biệt rõ bộ nhớ là RAM nha, còn thiết bị nhớ thì nói đến HDD, SSD, USB Memory...loại không bị xóa khi mất điện ấy để đỡ bị loạn)

Vì để chạy được ứng dụng thì phải load kernel vào bộ nhớ đầu, ta giả sử nhân Linux có kích thước khoảng 9MB đi. CPU không thể load chừng đó vào được.  
Cho dù có load được đi nữa thì cũng rất bất tiện, vì CPU chỉ thao tác thường là với một địa chỉ thường là cố định, nếu có thao tác được với thiết bị nhớ thì cũng rất giới hạn. Rất khó cho việc thay đổi.

Để giải quyết vấn đề này, người ta chia từ lúc cắm điện đến lúc nhân hệ điều hành được load vào bộ nhớ thành nhiều giai đoạn nối tiếp nhau:  
Kiểu như thế này

CPU --> LD 1 --> LD 2 --> LD 3 ...---> Hệ điều hành

CPU thực hiện load  **LD 1**,  **LD 1**  đưa vào bộ nhớ để chạy rồi cuối cùng nó thực hiện load  **LD 2**, rồi cứ thế, load hệ điều hành và chạy hệ điều hành.

Đến hệ điều hành rồi, thì ta sẽ có thể chạy được mọi thứ rồi.

Ở đây ta nên nhớ  **LD n-1**  thực hiện load xong  **LD n**, nó sẽ chuyển điều khiển (hay nhảy đến địa chỉ trên RAM mà nó đã load  **LD n**  vào để  **chạy**  luôn.  
Điều đó cũng có nghĩa, *_LD n - *_  trước đó sẽ kết thúc nhiệm vụ, không cần nữa.

Quá trình thực hiện  **LD 1 --> LD 2....--> LD N**  như ở trên được gọi chung là quá trình Booting, hay cả đống  **LD x**  kia được gọi là  `Bootloader`.

Có bao nhiêu lần  `load rồi thay thế`  sẽ phụ thuộc vào Platform cũng như Bootloader bạn sử dụng.

Nếu LD 1 để khả năng load hệ điều hành rồi, thì không cần đến LD 2, 3 nữa.

Nguyên lý có vẻ là vậy, nhưng thường các Bootloader được có 2, hoặc 3 lần là đến hệ điều hành rồi.

Các nhiệm vụ chính của bootloader:

-   Khởi tạo phần cứng
-   Thiết lập bộ nhớ RAM (DRAM)
-   Thiết lập bộ xử lý
-   Load hệ điều hành bằng cách đọc thiết bị nhớ, từ mạng, từ serial...

Trên Embedded Linux, bootloader được sử dụng phổ biến là Das U-Boot, Barebox.

Phổ biến nhất là Das U-Boot, rất nhiều chắc năng mạnh mẽ.

-   Có thể truy cập được các hệ thống file phổ biến như: FAT, ext2, ext3, ext4.
-   Hỗ trợ cả load kernel qua network nữa.
-   Hỗ trợ cơ chế truyền tham số cho kernel bằng device tree (cho ARM) khi boot kernel.

## 3\. Kernel - hệ điều hành bắt đầu từ đây

Kernel - Thành phần quan trọng nhất của hệ thống, chứa bộ lập lịch các tiến trình, quản lý bộ nhớ, quản lý thiết bị...etc.

**Được khởi động từ bootloader**  
Binary của Kernel được chứa trong 1 file. File chứa kernel thường có 2 loại là zImage (nén tự giải) và uImage ( phần header hỗ trợ việc boot từ Das U-Boot).

Sau khi được load lên địa chỉ bộ nhớ thích hợp, kernel sẽ được khởi động (theo mình hiểu đơn giản là JUMP đến địa chỉ bắt đầu để chạy thôi.  
Trước khi JUMP đến các giá trị tham số khởi động (một phần từ device tree) phải được truyền vào thông qua các thanh ghi (thường được quy định cho từng kiến trúc CPU).

**Board Support Package**

Để kernel chạy được trên phần cứng, thì phải có BSP (Board Support Package).  
BSP chứa các phần giao tiếp với phần cứng cụ thể, nó đóng vai trò trung gian cho hầu hết các lớp khác của Kernel và phần cứng.  
BSP có thể từ main-stream (tức là được tích hợp trong source của nhân Linux) hoặc từ chính các Vendor tạo ra phần cứng (các board).  
Các BSP này có thể được cung cấp qua các bản Patch.

**Kernel module**

Là thành phần phần mềm được load động vào kernel để chạy. Chạy ở kernel-space chứ không phải user-space.

Tùy vào cấu hình khi biên dịch kernel mà mỗi module, hoặc nhóm module sẽ được tích hợp sẵn vào bên trong kernel (file zImage hoặc uImage) hoặc được load khi hệ thống đang chạy.

Ứng dụng phổ biến của module là được sử dụng làm driver cho thiết bị.

Có một điểm chú ý liên quan đến license của một kernel module.  
Đó là module load vào ở dạng binary  
Dù đa số là mã nguồn mở, nhưng có một số kernel module được sử dụng kèm theo thiết bị lại ở dạng mã nguồn đóng, và chúng sẽ không được quản lý trên main stream.  
Cần chú ý cái này khi sử dụng kernel module dạng này trong các sản phẩm thương mại.

## 4\. User-space applications - với user đây là hệ thống

Là các ứng dụng từ init đến các ứng dụng đồ họa ta dùng.  
Đây là một phần quan trọng và không thể thiếu của hệ thống.  
Kernel sẽ là vô dụng nếu không có ứng dụng sử dụng các chức năng của kernel đó.  
Không tồn tại một hệ thống chỉ có kernel.

**Hệ thống file root**

Như ta đã biết, kernel (file zImage hoặc uImage) có thể được lưu bất cứ đâu.  
Nó chỉ là 1 file nằm trong 1 hệ thống file bất kì từ FAT, extN trên bất cứ thiết bị nào mà bootloader có thể đọc được, kể cả ở 1 NFS server có kết nối mạng đến thiết bị thật.

**Còn các ứng dụng thì sao??**  
Nó thường là một nhóm ứng dụng và nó phải nằm trong 1 hệ thống file.  
Hệ thống file này có thể nằm trên thiết bị nhớ hoặc trên bộ nhớ (trường hợp Init RAM fs)  
Khi được khởi động, hệ thống chỉ chạy duy nhất một root file system mà thôi.  
Được gọi là hệ thống file root, hệ thống file này có thể extN, JFFS2, ZFS, UBIFS...hỗ trợ các yêu cầu về hệ thống file cho Linux.

Có thể có một số hệ thống file nằm trên RAM mà không cần đến một thống file trên thiết bị lưu trữ. Nhưng vì chỉ tồn tại trên RAM, nên nó chỉ hữu ích trong một số tình huống nhất định như cứu hộ chẳng hạn..._init ram fs_  là một ví dụ.  
`initrd ram fs`  là hệ thống file chứa một số chương trình user-space, được bootloader  
load lên RAM cho kernel mount vào sử dụng như là hệ thống file root của nó.

Còn trong hầu hết hệ thống, việc đầu tiên mà kernel làm để tiếp cận với các ứng dụng  
là mount hệ thống file root (Tức gắn vào để dùng) . Vì thế, thông tin về thiết bị lưu trữ hệ thống file đó cũng phải được truyền cho kernel khi nó được khởi động. Đó là nhiệm vụ của  `bootloader`

**Chương trình Init**

Ứng dụng user-space đầu tiên được kernel chạy có tên là  _init program_.  
Không chỉ có 1 chương trình  _init program_. Mỗi lớp hệ thống Linux có một  _init program_  riêng.

Đó có thể là  **System V**  (phổ biến trên các distro desktop),  **systemd**  hoặc là  **BusyBox init**  (phổ biến trên Embedded Linux).

Vị trí (hay là đường dẫn) của  _init program_  trong hệ thống file root thường để set như là một tham số khi khởi động kernel. Nếu không được quét qua một tập được dẫn có sẵn trong source của Kernel để tìm.

Từ  `init program`  này, các chương trình khác sẽ được khởi động. Từ giao diện console thông qua serial đến ssh server.  
Mỗi loại  `init program`  lại có tính năng, tính dễ cấu hình, tính dễ thay đổi cũng khác nhau.

Đến đây, ta đã có thể sử dụng hệ thống như bao hệ thống Linux khác rồi.Tuy rằng, số chương trình có sẵn trong root file system của Embedded Linux ít hơn trên Desktop rất nhiều.

## Tham khảo

-   [ELCE 2010 Videos and Slides](http://free-electrons.com/blog/elce-2010-tutorial-videos/)  của tác giả Chris Simmonds Video từ free-electrons.com
-   [LazyTrick](https://lazytrick.wordpress.com/)


## Nguồn

https://kipalog.com/posts/4-thanh-phan-cua-Embedded-Linux

