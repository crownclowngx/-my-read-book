Add-Type -AssemblyName System.Drawing
$outDir = Join-Path $PSScriptRoot 'img'
[System.IO.Directory]::CreateDirectory($outDir) | Out-Null
$fontFamily = 'Microsoft YaHei UI'
$ink = [System.Drawing.ColorTranslator]::FromHtml('#182C43')
$muted = [System.Drawing.ColorTranslator]::FromHtml('#53677A')
$teal = [System.Drawing.ColorTranslator]::FromHtml('#087F8C')
function New-Canvas([int]$height) {
    $script:bitmap = [System.Drawing.Bitmap]::new(1600, $height)
    $script:g = [System.Drawing.Graphics]::FromImage($bitmap)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $g.Clear([System.Drawing.ColorTranslator]::FromHtml('#F5F8FB'))
}
function Text([string]$s, [float]$x, [float]$y, [float]$size=26, $color=$ink, [float]$width=1450, [float]$height=120, [bool]$bold=$false) {
    $style = if ($bold) { [System.Drawing.FontStyle]::Bold } else { [System.Drawing.FontStyle]::Regular }
    $font = [System.Drawing.Font]::new($fontFamily, $size, $style, [System.Drawing.GraphicsUnit]::Pixel)
    $brush = [System.Drawing.SolidBrush]::new($color)
    $rect = [System.Drawing.RectangleF]::new($x,$y,$width,$height)
    $g.DrawString($s,$font,$brush,$rect)
    $font.Dispose(); $brush.Dispose()
}
function Card([float]$x,[float]$y,[float]$w,[float]$h,[string]$fill) {
    $brush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml($fill))
    $g.FillRectangle($brush,$x,$y,$w,$h)
    $brush.Dispose()
}
function Save([string]$name) {
    $bitmap.Save((Join-Path $outDir $name),[System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bitmap.Dispose()
}
New-Canvas 1370
Text 'DeepInfer 影响世界的中间条件' 70 45 44 $ink 1460 70 $true
Text '概念传导图  |  每一步都需要独立证据' 72 118 25 $muted
$items = @(
    @('公开技术','推理核心与两条硬件路线','起点：公开资料'),
    @('稳定服务','补齐外围系统并持续运营','条件：供货、运维、峰值容量'),
    @('经济替代','同等业务质量下总成本可接受','条件：成功率、利用率、API 价格'),
    @('采购选择','客户可以迁移，也可以据此议价','条件：迁移费用、合同、产品差异'),
    @('产业变化','收入结构与利润分配调整','观察：续约、实际用量、单位利润'),
    @('长期影响','融资估值与区域依赖可能调整','条件：需求、现金流、政策与设施')
)
for ($i=0; $i -lt $items.Count; $i++) {
    $y = 205 + $i * 174
    Card 72 $y 1456 136 '#FFFFFF'
    Card 72 $y 9 136 '#087F8C'
    Text ('0' + ($i+1)) 105 ($y+20) 36 $teal 75 70 $true
    Text $items[$i][0] 210 ($y+18) 31 $ink 270 55 $true
    Text $items[$i][1] 500 ($y+19) 29 $ink 990 60
    Text $items[$i][2] 500 ($y+76) 24 $muted 990 50
    if ($i -lt 5) {
        $pen = [System.Drawing.Pen]::new($teal,3)
        $pen.EndCap = [System.Drawing.Drawing2D.LineCap]::ArrowAnchor
        $g.DrawLine($pen, 142, $y+141, 142, $y+169)
        $pen.Dispose()
    }
}
Text '技术公开扩大选项；可持续的商业替代决定影响大小。' 72 1270 25 $muted
Save '01-影响传导.png'

New-Canvas 1150
Text 'DeepInfer 与 AI 服务的四种未来' 70 45 44 $ink 1460 70 $true
Text '条件情景  |  不是概率预测，也不是已发生的市场结果' 72 118 25 $muted
Text '开放部署的商业替代能力' 610 190 29 $ink 750 50 $true
Text '弱' 530 252 30 $muted 100 50 $true
Text '强' 1150 252 30 $teal 100 50 $true
Text '闭源前沿' 65 400 26 $ink 180 50 $true
Text '能力优势' 65 440 26 $ink 180 50 $true
Text '强' 125 330 32 $teal 80 60 $true
Text '弱' 125 705 32 $muted 80 60 $true
$cards = @(
    @(270,320,'C  集中式平台继续占优','完整服务门槛与能力差距','共同维持集中','#E8EEF5'),
    @(910,320,'A  开放与前沿服务分工','常规任务采用开放部署','困难任务购买前沿服务','#DDF2EF'),
    @(270,690,'D  运营平台成为整合者','模型差异缩小，客户仍依赖','成熟平台的交付能力','#E8EEF5'),
    @(910,690,'B  模型服务价格竞争','通用能力更容易替代','利润依赖运营、产品和分发','#E1ECFA')
)
foreach ($c in $cards) {
    Card $c[0] $c[1] 590 300 $c[5]
    Text $c[2] ($c[0]+32) ($c[1]+35) 30 $ink 530 90 $true
    Text $c[3] ($c[0]+32) ($c[1]+143) 27 $muted 530 65
    Text $c[4] ($c[0]+32) ($c[1]+194) 27 $muted 530 65
}
Text '各情景仍受硬件供货、能源、运维与政策影响。' 270 1040 25 $muted
Save '02-未来情景.png'

New-Canvas 1180
Text '中国视角下的 DeepInfer 影响路径' 70 45 44 $ink 1460 70 $true
Text '条件推演  |  国内应用与国际合作分别检验' 72 118 25 $muted
Card 72 205 1456 105 '#FFFFFF'
Text '共同起点：完整服务稳定，同等业务质量下成本可接受' 105 238 32 $ink 1390 60 $true
Card 72 365 700 500 '#DDF2EF'
Card 812 365 716 500 '#E1ECFA'
Text '对内：应用与供给能力' 105 400 33 $ink 630 65 $true
Text '行业应用与实际流程改善' 105 490 29 $ink 630 65
Text '付费负载与运行反馈' 105 570 29 $ink 630 65
Text '引擎、算子与硬件持续改进' 105 650 29 $ink 630 65
Text '条件：组织改造、供货、利用率' 105 765 25 $muted 630 70
Text '对外：选择与合作空间' 845 400 33 $ink 650 65 $true
Text '海外复现与当地独立运营' 845 490 29 $ink 650 65
Text '技术协作、培训与持续服务' 845 570 29 $ink 650 65
Text '影响力与商业收入分别验证' 845 650 29 $ink 650 65
Text '条件：信任、本地团队、市场准入' 845 765 25 $muted 650 70
Card 72 920 1456 155 '#FFFFFF'
Text '三本账：国内业务收益  /  中国供应商收入  /  关键服务韧性' 105 946 30 $ink 1390 60 $true
Text '海外竞争者也会受益；中国内部各环节可能得失分化。' 105 1009 26 $muted 1390 55
Text '技术采用增加，不自动等于国产硬件份额或中国企业收入增加。' 72 1105 25 $muted
Save '03-中国影响路径.png'
Write-Output $outDir
