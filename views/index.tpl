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
					<i class="fa fa-home icon" aria-hidden="true"></i>
					<div class="breadcrumb">Startseite</div>
					<h2>{{haus}}</h2>
				</div>
			</div>
		</div>
		<div class="container">
			<div class="row">	
				<table class="u-full-width">
					<tbody>
					% for etage in allEtagen:
						<tr>
							<td class="switch">
								<div class="onoffswitch">
									% checked = ' checked' if etage['eingeschaltet'] == 1 else ''
									<input type="checkbox" data-link="{{etage['etage_link']}}" class="onoffswitch-checkbox" id="switch_{{etage['etage_link']}}"{{checked}}>
									<label class="onoffswitch-label" for="switch_{{etage['etage_link']}}"></label>
								</div>
							</td>
							<td data-link="{{etage['etage_link']}}">
								{{etage['name']}}
							</td>
							<td data-link="{{etage['etage_link']}}" class="chevron">
								<i class="fa fa-fw fa-chevron-right" aria-hidden="true"></i>
							</td>
							</tr>
					% end
					% if len(allEtagen) == 0:
						<tr>
							<td>
								Keine Etagen in diesem Haus vorhanden.
							</td>
						</tr>
					% end					
					</tbody>
				</table>
			</div>
		</div>
		<script>
			$(function(){
				$('td[data-link]').on('click', function(){
					window.location.href = "/" + $(this).attr('data-link');
				});
				$(':checkbox').change(function(){
					url = "/" + $(this).attr('data-link') + "/eingeschaltet";
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