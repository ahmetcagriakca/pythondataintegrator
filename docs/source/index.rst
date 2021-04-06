.. JediContributors PDI documentation master file, created by JediContributors

Welcome to Python Data Integrator documentation!
====================================


.. image:: images/logo.png
   :align: center
   
.. warning:: 
   Warning information blabla
   
.. note:: This docs cover the latest version on main branch. This might not be released yet. Use the version picker in the lower left corner to select docs for a specific version.

It enables the following features in your applications:


| **What is Lorem Ipsum Yasin?** 
| Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
when an unknown printer took a galley of type and scrambled it to make a type specimen book.
It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. 
It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum


.. code-block:: csharp

    var migrationCommands = _migrationsSqlGenerator.Generate(prioritizedMigrationOperationList.OrderByDescending(o => o.RefHitCount).Select(s => s.Migration).ToList());
                var preSql = string.Join("\n\r\n\r", migrationCommands.Select(s => s.CommandText));

                migrationCommands = _migrationsSqlGenerator.Generate(migrationOperationList.OrderByDescending(o => o.RefHitCount).Select(s => s.Migration).ToList());
                var midSql = string.Join("\n\r\n\r", migrationCommands.Select(s => s.CommandText));

                migrationCommands = _migrationsSqlGenerator.Generate(latestMigrationOperationList.OrderByDescending(o => o.RefHitCount).Select(s => s.Migration).ToList());
                var postSql = string.Join("\n\r\n\r", migrationCommands.Select(s => s.CommandText));

                var sql = string.Join("\n\r\n\r", preSql, midSql, postSql);
                return SuccessDataResult(sql);
				
				 //TODO: check constraint changes
                    var ConstraintDiffOperations = _migrationOperationService.GetConstraintDiffOperations(currVersion, oldVersion);
                    prioritizedMigrationOperationList.AddRange(ConstraintDiffOperations.Where(w => (w.Migration is DropCheckConstraintOperation || w.Migration is DropUniqueConstraintOperation)));
                    latestMigrationOperationList.AddRange(columnDiffOperations.Where(w => (w.Migration is CreateCheckConstraintOperation || w.Migration is AddUniqueConstraintOperation)));

                    //TODO: Primary key 
                    migrationOperationList.AddRange(_migrationOperationService.GetPrimaryKeycChangeOperations(currVersion, oldVersion));

                    await _entityService.SetEntityStatus(Guid.Parse(currVersion.Id), EntityVersionStatus.SentToProduction);
   
.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: Getting Started
   
   gettingstarted/whatispdi
   gettingstarted/architecture
   
.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: Contributing & License
   
   contributing/license
   contributing/howicontribute

