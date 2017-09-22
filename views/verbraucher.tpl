<!doctype html>
<html lang="de">
	<head>
		<meta charset="utf-8">
		<meta http-equiv="x-ua-compatible" content="ie=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<link rel="icon" href="/favicon.ico">
		
		<title>Lichtsteuerung</title>

		<link rel="stylesheet" href="/css/normalize.css">
		<link rel="stylesheet" href="/css/skeleton.css">
		<link rel="stylesheet" href="/css/fontawesome.css">
		<link rel="stylesheet" href="/css/rangeslider.css">
		<link rel="stylesheet" href="/css/puls.css">
		
		<script src="/js/jquery.js"></script>
		<script src="/js/rangeslider.js"></script>
	</head>
	<body>
		<div class="header">
			<div class="container">
				<div class="row">
					<div class="twelve columns">
						<i class="fa fa-wrench icon" aria-hidden="true"></i>
						<div class="breadcrumb">
							<a href="/">{{haus}}</a>
							<b>&nbsp;&#183;&nbsp;</b> 
							<a href="/{{etage['etage_link']}}">{{etage['name']}}</a>
							<b>&nbsp;&#183;&nbsp;</b>
							<a href="/{{etage['etage_link']}}/{{zimmer['zimmer_link']}}">{{zimmer['name']}}</a>
						</div>
						<h2>{{verbraucher['name']}}</h2>
					</div>
				</div>
			</div>
		</div>
	
		<div class="container">
			<div class="row">	
				<div class="twelve columns">
					<table class="u-full-width">
						<tbody>							
							% if verbraucher['typ'] == 'S':
							<tr>
								<td colspan="2">
									<b>Keine Einstellmöglichkeiten vorhanden</b>
								</td>
							</tr>
							% end
							% if verbraucher['typ'] == 'L':
							<tr>
								<td style="width: 33%">
									Helligkeit
								</td>
								<td>
									<input type="range" min="0" max="4096" step="1" value="{{verbraucher['helligkeit']}}">
								</td>
							</tr>
							<tr>
								<td style="width: 33%">
									Modus
								</td>
								<td>
									<select class="u-full-width" id="modus">
									% for mode in modi:
										% selected = ' selected' if mode[0] == verbraucher['modus'] else ""
										<option value="{{mode[0]}}"{{selected}}>{{mode[1]}}</option>
									% end
									</select>
								</td>
							</tr>
							% end
							<tr>
								<td style="width: 33%">
									Aktueller Zustand
								</td>
								<td>
								% if etage['eingeschaltet'] == 1 and zimmer['eingeschaltet'] == 1 and verbraucher['eingeschaltet'] == 1:
									<b>Eingeschaltet</b>
								% else: 
									<b>Ausgeschaltet</b>
								% end
								</td>
							</tr>
							<tr>
								<td style="width: 33%">
									Typ / Anschluss
								</td>
								<td>
									% if verbraucher['typ'] == 'L':
									<b>Dimmer</b>&nbsp;/&nbsp;
									% end
									% if verbraucher['typ'] == 'S':
									<b>Relais</b>&nbsp;/&nbsp;
									% end
									Modul : <b>{{verbraucher['modul']}}</b>&nbsp;&nbsp;Anschluss : <b>{{verbraucher['port']}}</b>
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>
			<div class="row">
				<div class="twelve columns">
					<a class="button button-primary u-pull-right" href="/{{etage['etage_link']}}/{{zimmer['zimmer_link']}}">Zurück</a>
				</div>
			</div>
		</div>
		<script>
			$('input[type="range"]').rangeslider({
				polyfill: false,
				onSlideEnd: function(position, value) {
					url = "/{{etage['etage_link']}}/{{zimmer['zimmer_link']}}/{{verbraucher['verbraucher_link']}}/helligkeit";
					$.ajax({
						type: "POST",
						url: url,
						data: { value: value }
					});	
				}
			});
			$('#modus').change(function(){
				url = "/{{etage['etage_link']}}/{{zimmer['zimmer_link']}}/{{verbraucher['verbraucher_link']}}/modus";
				$.ajax({
					type: "POST",
					url: url,
					data: { value: $(this).val() }
				});	
			});
		</script>
	</body>
</html>