. (Join-Path $PSScriptRoot '绘图.ps1') | Out-Null

New-Canvas 1100
Text '私有部署的成本临界点会随竞争变化' 70 40 42 $ink 1480 70 $true
Text '假设算例  |  不代表 DeepInfer 实测成本或实际产品价格' 72 115 25 $muted
$x0=165; $x1=1480; $y0=850; $y1=250
$grid=[System.Drawing.Pen]::new([System.Drawing.ColorTranslator]::FromHtml('#DDE5ED'),1)
for($i=0;$i -le 4;$i++) {
    $x=$x0+($x1-$x0)*$i/4
    $y=$y0-($y0-$y1)*$i/4
    $g.DrawLine($grid,[float]$x,[float]$y0,[float]$x,[float]$y1)
    $g.DrawLine($grid,[float]$x0,[float]$y,[float]$x1,[float]$y)
    Text ([string]($i*10)) ($x-15) ($y0+20) 24 $muted 90 45
    Text ([string]($i*10)) 90 ($y-16) 24 $muted 80 45
}
$grid.Dispose()
Text '月成本（万元）' 70 195 26 $ink 400 45
Text '每月标准任务量（万）' 1060 920 26 $ink 450 50
$lines=@(@(1.0,0,'#BC6B21'),@(0.6,0,'#8063AA'),@(0.25,100000,'#087F8C'))
foreach($line in $lines) {
    $pen=[System.Drawing.Pen]::new([System.Drawing.ColorTranslator]::FromHtml($line[2]),5)
    $pts=[System.Drawing.PointF[]]@(
        [System.Drawing.PointF]::new($x0,($y0-($line[1]/400000)*($y0-$y1))),
        [System.Drawing.PointF]::new($x1,($y0-(($line[1]+$line[0]*400000)/400000)*($y0-$y1)))
    )
    $g.DrawLines($pen,$pts); $pen.Dispose()
}
foreach($q in @((100000/(1-.25)),(100000/(.6-.25)))) {
    $px=$x0+($q/400000)*($x1-$x0)
    $py=$y0-((100000+.25*$q)/400000)*($y0-$y1)
    $brush=[System.Drawing.SolidBrush]::new($ink)
    $g.FillEllipse($brush,($px-7),($py-7),14,14); $brush.Dispose()
}
Text '13.33 万任务' 510 586 25 $ink 360 50 $true
Text '28.57 万任务' 1040 520 25 $ink 360 50 $true
Text 'API：1.00 元 / 任务' 165 170 26 ([System.Drawing.ColorTranslator]::FromHtml('#BC6B21')) 430 50 $true
Text 'API：0.60 元 / 任务' 650 170 26 ([System.Drawing.ColorTranslator]::FromHtml('#8063AA')) 430 50 $true
Text '私有：10 万 + 0.25Q' 1120 170 26 $teal 440 50 $true
Text '假设双方业务质量相同；未模拟容量扩展阶梯与峰值流量。' 165 1000 25 $muted 1350 60
Save '04-成本临界点.png'

New-Canvas 1200
Text '应用发展与制造产业化的不同阶段' 70 45 44 $ink 1460 70 $true
Text '乐观条件情景  |  样机不是量产结果，后续未指定完成年份' 72 118 25 $muted
$rows=@(
    @('2026—2030','可交付硬件与开放软件','持续供货、服务成熟、业务采用','积累客户、人才与运行经验','#DDF2EF'),
    @('2030 年前','EUV 工程样机','本文设定的乐观假设','增加后续制造选择与验证条件','#E1ECFA'),
    @('后续阶段','工艺验证与经济量产','可靠性、吞吐、材料、良率等继续推进','才能进一步影响先进芯片成本与产能','#E8EEF5')
)
for($i=0;$i -lt $rows.Count;$i++) {
    $y=220+$i*245
    Card 72 $y 1456 205 $rows[$i][4]
    Text $rows[$i][0] 105 ($y+28) 31 $teal 280 65 $true
    Text $rows[$i][1] 430 ($y+25) 32 $ink 1050 60 $true
    Text $rows[$i][2] 430 ($y+90) 28 $ink 1050 60
    Text $rows[$i][3] 430 ($y+145) 26 $muted 1050 60
}
Card 72 1000 1456 120 '#FFFFFF'
Text '应用可以先发展；后续制造成熟，有机会增强已有体系的扩展能力。' 105 1035 29 $ink 1380 70 $true
Save '05-制造与应用时间.png'
