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
		<link rel="stylesheet" href="/css/puls.css">
		
		<script src="/js/jquery.js"></script>
	</head>
	<body>
		<div class="header">
			<div class="container">
				<div class="row">
					<i class="fa fa-lightbulb-o icon" aria-hidden="true"></i>
					<div class="breadcrumb">
						<a href="/">{{haus}}</a>
						<b>&nbsp;&#183;&nbsp;</b> 
						<a href="/{{etage['etage_link']}}">{{etage['name']}}</a>
					</div>
					<h2>{{zimmer['name']}}</h2>
				</div>
			</div>
		</div>
		<div class="container">
			<div class="row">	
				<table class="u-full-width">
					<tbody>
					% for verbraucher in allVerbraucher:
						<tr>
							<td class="switch">
								<div class="onoffswitch">
									% checked = ' checked' if verbraucher['eingeschaltet'] == 1 else ''
									<input type="checkbox" data-link="{{verbraucher['verbraucher_link']}}" class="onoffswitch-checkbox" id="switch_{{verbraucher['verbraucher_link']}}"{{checked}}>
									<label class="onoffswitch-label" for="switch_{{verbraucher['verbraucher_link']}}"></label>
								</div>
							</td>
							<td data-link="{{verbraucher['verbraucher_link']}}">
								{{verbraucher['name']}}									
							</td>
							<td data-link="{{verbraucher['verbraucher_link']}}" class="chevron">
								<i class="fa fa-fw fa-chevron-right" aria-hidden="true"></i>
							</td>
						</tr>
					% end
					% if len(allVerbraucher) == 0:
						<tr>
							<td>
								Keine Verbraucher in diesem Zimmer vorhanden.
							</td>
						</tr>
					% end
					</tbody>
				</table>
			</div>
			<div class="row">
				<a class="button button-primary u-pull-right" href="/{{etage['etage_link']}}">Zurück</a>
			</div>
		</div>
		<script>
			$(function(){
				$('td[data-link]').on('click', function(){
					window.location.href = "/{{etage['etage_link']}}/{{zimmer['zimmer_link']}}/" + $(this).attr('data-link');
				});
				$(':checkbox').change(function(){
					url = "/{{etage['etage_link']}}/{{zimmer['zimmer_link']}}/" + $(this).attr('data-link') + "/eingeschaltet";
					data = $(this).is(':checked') ? '1' : '0';
					$.ajax({
						type: "POST",
						url: url,
						data: { value: data }
					});					
				});
			});
		</script>		
	</body>
</html>